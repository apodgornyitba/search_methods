import heapq
from node import Node
from frontier import PriorityQueue
from fill_zone import FillZone, GameStatus
from gamecolor import Color
from game_parser import Parser

import copy
import time
import sys
import os
import csv

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
    
    def print_game_statistics(self, algorithm: str, result: str, cost: int, expanded_nodes: int, frontier_nodes: int, solution, time_elapsed, heuristic=None):
        print('- Algorithm: {}'.format(algorithm))
        print('- Result: {}'.format(result))
        print('- Cost: {}'.format(cost))
        print('- Expanded Nodes: {}'.format(expanded_nodes))
        print('- Frontier Nodes: {}'.format(frontier_nodes))
        print('- Solution: {}'.format(solution))
        print('- Time elapsed: {}'.format(time_elapsed))
        if heuristic is not None:
            print('- Heuristic: {}'.format(heuristic))
        print('\n')


    def to_file(self, algorithm: str, result: str, grid_size: int, cost: int, expanded_nodes: int, frontier_nodes: int, time_elapsed, heuristic=None):
        if not os.path.exists('results'):
            os.makedirs('results')
        if not os.path.isfile('results/output{}.csv'.format(grid_size)):
            with open('results/output{}.csv'.format(grid_size), 'a', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['Algorithm', 'Result', 'Cost', 'Expanded Nodes', 'Frontier Nodes', 'Time elapsed', 'Heuristic'])
        with open('results/output{}.csv'.format(grid_size), 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([algorithm, result, cost, expanded_nodes, frontier_nodes, time_elapsed, heuristic])

    def uninformed_method(self, algorithm, grid_size: int, grid, color_amount: int, turns: int, input_file: str = None):
        self.num_explored = 0
        actions = []
        result = 'LOSS'
        cost = None
        parser = Parser()

        start_time = time.time()

        starting_color = grid[0][0]         # Saving it bc algotirhm overrides it
        initial_state = FillZone(grid_size, grid, color_amount, turns)
        starting_zone = initial_state.current_color_cells

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

        algorithm = algorithm.name
        self.to_file(algorithm, len(grid), result, cost, self.num_explored, len(frontier.frontier), end_time - start_time)
        for cell in starting_zone:
            grid[cell[0]][cell[1]] = starting_color
        if not input_file is None:
            parser.generate_solution_file(algorithm, grid, input_file, actions)
        else:
            parser.generate_solution_file(algorithm=algorithm, input_file = None, grid= grid,solution= actions)

    
    def informed_method(self, algorithm: str, grid_size: int, grid, color_amount: int, turns: int, heuristic, input_file: str = None):
        self.num_explored = 0
        actions = []
        result = 'LOSS'
        cost = None
        parser = Parser()

        starting_color = grid[0][0]         # Saving it bc algotirhm overrides it

        start_time = time.time()

        initial_state = FillZone(grid_size, grid, color_amount, turns)
        starting_zone = initial_state.current_color_cells

        start = Node(state=initial_state, parent=None, action=None)
        frontier = PriorityQueue()
        if heuristic == 'remaining_colors_heuristic':
            frontier.add((start, globals()[heuristic](start.state.grid, color_amount)))
        elif heuristic == 'color_fraction_heuristic':
            frontier.add((start, globals()[heuristic](start.state.grid, grid_size)))
        else:
            frontier.add((start, globals()[heuristic](grid_size, start.state.current_color_cells)))
            
        # Initialize an empty explored set
        self.explored = set()
        while True:
            if frontier.empty():
                break
            n = frontier.remove()
            self.num_explored += 1

            # If node is the goal, then we have a solution
            if n[0].state.game_status == GameStatus.WIN:
                result = 'WIN'
                while n[0].parent is not None:
                    actions.append(n[0].action.name)
                    n = n[0].parent
                actions.reverse()
                self.solution = actions
                cost = len(actions)
                break

            # Mark node as explored
            self.explored.add(n[0].state)

            # If game finished, don't expand solution
            if n[0].state.game_status == GameStatus.LOSS:
                continue

            # Add neighbors to frontier
            for action, state in self.neighbors(n[0].state):
                if not frontier.contains_state(state) and state not in self.explored:
                    child = Node(state=state, parent=n, action=action, cost=n[0].cost + 1)
                    if algorithm == 'greedy':
                        if heuristic == 'remaining_colors_heuristic':
                            frontier.add((child, globals()[heuristic](child.state.grid, color_amount)))
                        elif heuristic == 'color_fraction_heuristic':
                            frontier.add((child, globals()[heuristic](child.state.grid, grid_size)))
                        else:
                            frontier.add((child, globals()[heuristic](grid_size, child.state.current_color_cells)))
                    elif algorithm == 'astar':
                        if heuristic == 'remaining_colors_heuristic':
                            frontier.add((child, child.cost + globals()[heuristic](child.state.grid, color_amount)))
                        elif heuristic == 'color_fraction_heuristic':
                            frontier.add((child, child.cost + globals()[heuristic](child.state.grid, grid_size)))
                        else:
                            frontier.add((child, child.cost + globals()[heuristic](grid_size, child.state.current_color_cells)))
                            
        end_time = time.time()
        self.to_file(algorithm, result, len(grid), cost, self.num_explored, len(frontier.frontier), end_time - start_time, heuristic)
        for cell in starting_zone:
            grid[cell[0]][cell[1]] = starting_color
        if not input_file is None:
            parser.generate_solution_file(algorithm, grid, input_file, actions)
        else:
            parser.generate_solution_file(algorithm=algorithm, input_file = None, grid= grid,solution= actions)


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

def bronson_distance_heuristic(grid_size, current_color_cells):
    # Busca la celda más alejada
    max_distance = 0
    farthest_cell = None
    for i in range(grid_size):
        for j in range(grid_size):
            if not (i,j) in current_color_cells:
                distance = min(i, j, grid_size-1, grid_size-1)
                if distance > max_distance:
                    max_distance = distance
                    farthest_cell = (i, j)
    if farthest_cell is None:
        return 0  # Ya se terminó el juego
    
    # Crea un grafo de las celdas no controladas
    graph = {}
    for i in range(grid_size):
        for j in range(grid_size):
            if not (i,j) in current_color_cells:
                neighbors = []
                if i > 0:
                    neighbors.append(((i-1, j), 1))
                if i < grid_size-1:
                    neighbors.append(((i+1, j), 1))
                if j > 0:
                    neighbors.append(((i, j-1), 1))
                if j < grid_size-1:
                    neighbors.append(((i, j+1), 1))
                graph[(i, j)] = neighbors
            else:
                graph[(i, j)] = []

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


