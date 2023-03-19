from node import Node
from frontier import DeepFirstSearch, BreadthFirstSearch
from fill_zone import FillZone, GameStatus
from gamecolor import Color
from parserInput import Parser

import copy
import time
import sys
import random

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
    
    def generate_random_grid(self, grid_size: int, color_amount: int):
        grid = []
        for i in range(grid_size):
            row = []
            for j in range(grid_size):
                row.append(Color(random.randint(0, color_amount - 1)))
            grid.append(row)
        return grid

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
