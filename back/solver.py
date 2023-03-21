from queue import PriorityQueue
from node import Node
from frontier import DeepFirstSearch, BreadthFirstSearch
from fill_zone import FillZone, GameStatus
from gamecolor import Color
from parserInput import Parser

import copy
import time
import sys
import heapq

class Solver:
    def __init__(self):
        pass

    def neighbors(self, state: FillZone):
        candidates = []
        next_state = None

        for color in Color:                                 # Loading possible candidates from actual state
            if state.current_color != color:                # Choosing the same color as before is an invalid action
                next_state = copy.deepcopy(state)
                next_state.change_color(color)
                candidates.append((color, next_state))
        
        return candidates
    
    def print_game_statistics(self, algorithm: str, result: str, cost: int, expanded_nodes: int, frontier_nodes: int, solution, time_elapsed):
        print('- Algorithm: {}'.format(algorithm))
        print('- Result: {}'.format(result))
        print('- Cost: {}'.format(cost))
        print('- Expanded Nodes: {}'.format(expanded_nodes))
        print('- Frontier Nodes: {}'.format(frontier_nodes))
        print('- Solution: {}'.format(solution))
        print('- Time elapsed: {}'.format(time_elapsed))
        print()


    def uninformed_method(self, algorithm: DeepFirstSearch, grid_size: int, grid, color_amount: int, turns: int):
        self.num_explored = 0
        actions = []
        result = 'LOSS'
        cost = None

        start_time = time.time()

        initial_state = FillZone(grid_size, grid, color_amount, turns)
        start = Node(state=initial_state, parent=None, action=None)
        frontier = algorithm
        frontier.add(start)

        # Initialize an empty explored set
        self.explored = set()

        # Keep looping until solution found
        while True:

            # If nothing left in frontier, then no path
            if frontier.empty():
                break

            # Choose a node from the frontier
            node = frontier.remove()
            self.num_explored += 1

            # If node is the goal, then we have a solution
            if node.state.game_status == GameStatus.WIN:
                result = 'WIN'
                while node.parent is not None:
                    actions.append(node.action.name)
                    node = node.parent
                actions.reverse()
                self.solution = actions
                cost = len(actions)
                break

            # Mark node as explored
            self.explored.add(node.state)

            # If game finished, don't expand solution
            if node.state.game_status == GameStatus.LOSS:
                # print('Game ended for action {}'.format(node.action))
                continue

            # Add neighbors to frontier
            for action, state in self.neighbors(node.state):
                if not frontier.contains_state(state) and state not in self.explored:
                    child = Node(state=state, parent=node, action=action)
                    frontier.add(child)
        end_time = time.time()

        algorithm = 'DFS'
        if isinstance(algorithm, BreadthFirstSearch):
            algorithm = 'BFS' 
        self.print_game_statistics(algorithm, result, cost, self.num_explored, len(frontier.frontier), actions, end_time - start_time)
    
    def greedy(self, grid_size: int, grid, color_amount: int, turns: int, heuristic):
        self.num_explored = 0
        actions = []
        result = 'LOSS'
        cost = None

        start_time = time.time()

        initial_state = FillZone(grid_size, grid, color_amount, turns)
        start = Node(state=initial_state, parent=None, action=None)
        frontier = PriorityQueue()
        frontier.add(start, heuristic(start.state.grid, grid_size))
        # Initialize an empty explored set
        self.explored = set()
        while True:
            if (len(frontier) == 0):
                break
            n = frontier.get()
            self.num_explored += 1

            # If node is the goal, then we have a solution
            if n.state.game_status == GameStatus.WIN:
                result = 'WIN'
                while n.parent is not None:
                    actions.append(n.action.name)
                    n = n.parent
                actions.reverse()
                self.solution = actions
                cost = len(actions)
                break

            # Mark node as explored
            self.explored.add(n.state)

            # If game finished, don't expand solution
            if n.state.game_status == GameStatus.LOSS:
                continue

            # Add neighbors to frontier
            for action, state in self.neighbors(n.state):
                if not frontier.contains_state(state) and state not in self.explored:
                    child = Node(state=state, parent=n, action=action)
                    frontier.add(child, heuristic(child.state.grid, grid_size))
        end_time = time.time()

        self.print_game_statistics('Greedy', result, cost, self.num_explored, len(frontier.frontier), actions, end_time - start_time)

def remaining_colors_heuristic(grid, color_amount):
    colors = set()
    for row in grid:
        for color in row:
            colors.add(color)
            if len(colors) == color_amount:
                break
    return len(colors)


def color_fraction_heuristic(grid, grid_size):
    total_cells = grid_size * grid_size
    color_counts = {}
    for row in grid:
        for color in row:
            if color is not None:
                if color in color_counts:
                    color_counts[color] += 1
                else:
                    color_counts[color] = 1
    color_fractions = [count / total_cells for count in color_counts.values()]
    heuristic = sum(color_fractions)
    return heuristic

def bronson_distance_heuristic(grid, grid_size):
    # Busca la celda más alejada
    max_distance = 0
    farthest_cell = None
    for i in range(grid_size):
        for j in range(grid_size):
            if grid[i][j] is None:
                distance = min(i, j, grid_size-i-1, grid_size-j-1)
                if distance > max_distance:
                    max_distance = distance
                    farthest_cell = (i, j)
    if farthest_cell is None:
        return 0  # Ya se terminó el juego

    # Crea un grafo de las celdas no controladas
    graph = {}
    for i in range(grid_size):
        for j in range(grid_size):
            if grid[i][j] is None:
                neighbors = []
                if i > 0 and grid[i-1][j] is None:
                    neighbors.append(((i-1, j), 1))
                if i < grid_size-1 and grid[i+1][j] is None:
                    neighbors.append(((i+1, j), 1))
                if j > 0 and grid[i][j-1] is None:
                    neighbors.append(((i, j-1), 1))
                if j < grid_size-1 and grid[i][j+1] is None:
                    neighbors.append(((i, j+1), 1))
                graph[(i, j)] = neighbors

    # Utiliza Dijkstra para encontrar la distancia mínima entre cada celda y la celda más alejada del borde
    distances = {cell: sys.maxsize for cell in graph.keys()}
    distances[farthest_cell] = 0
    heap = [(0, farthest_cell)]
    while heap:
        (distance, current) = heapq.heappop(heap)
        if distance > distances[current]:
            continue
        for (neighbor, weight) in graph[current]:
            new_distance = distance + weight
            if new_distance < distances[neighbor]:
                distances[neighbor] = new_distance
                heapq.heappush(heap, (new_distance, neighbor))

    # Toma el valor máximo de las distancias encontradas como la heurística
    heuristic = max(distances.values())
    return heuristic

    

if __name__ == "__main__":
    n = len(sys.argv)
    turns = 30
    if n < 2 or n > 3:
        raise Exception('Only Grid size and optionally turns must be provided as argument')
    if n == 3:
        turns = int(sys.argv[2])

    parser = Parser()
    (color_amount, grid) = Parser.parse_color_file(sys.argv[1])
    grid_size = len(grid)

    solver = Solver()
    dfs = DeepFirstSearch()
    bfs = BreadthFirstSearch()

    solver.uninformed_method(dfs, grid_size, grid, color_amount, turns)

    solver.uninformed_method(bfs, grid_size, grid, color_amount, turns)

    solver.greedy(grid_size, grid, color_amount, turns, remaining_colors_heuristic)
