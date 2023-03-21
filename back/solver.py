from node import Node
from frontier import DeepFirstSearch, BreadthFirstSearch
from fill_zone import FillZone, GameStatus
from gamecolor import Color, HexColor
from game_parser import Parser

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


    def uninformed_method(self, algorithm, grid_size: int, grid, color_amount: int, turns: int, input_file: str = None):
        self.num_explored = 0
        actions = []
        result = 'LOSS'
        cost = None

        start_time = time.time()

        starting_color = grid[0][0]         # Saving it bc algotirhm overrides it

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

        algorithm = algorithm.name
        self.print_game_statistics(algorithm, result, cost, self.num_explored, len(frontier.frontier), actions, end_time - start_time)
        grid[0][0] = starting_color
        if not input_file is None:
            parser.generate_solution_file(algorithm, grid, input_file, actions)
        else:
            parser.generate_solution_file(algorithm=algorithm, input_file = None, grid= grid,solution= actions)
    
def generate_random_grid(grid_size: int, color_amount: int):
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
    input_file = None
    
    if n > 5:
        raise Exception('Only Grid size and optionally turns must be provided as argument')

    parser = Parser()

    match sys.argv[1]:    
        case '-r':
            if sys.argv[2] is None or int(sys.argv[2]) <= 0:
                raise Exception('Invalid grid size')
            grid_size = int(sys.argv[2])
            if sys.argv[3] is None or int(sys.argv[3]) <= 0:
                raise Exception('Invalid color amount')
            color_amount = int(sys.argv[3])
            if sys.argv[4] is None or int(sys.argv[4]) <= 0:
                raise Exception('Invalid turn amount')
            turns = int(sys.argv[4])
            grid = generate_random_grid(grid_size, color_amount)
        case _:
            if sys.argv[1] is None:
                raise Exception('Invalid file path')
            if sys.argv[2] is None:
                raise Exception('Invalid turn amount')
            (color_amount, grid) = Parser.parse_color_file(sys.argv[1])
            grid_size = len(grid)
            input_file = sys.argv[1]
            turns = int(sys.argv[2])

    solver = Solver()
    dfs = DeepFirstSearch()
    bfs = BreadthFirstSearch()

    solver.uninformed_method(dfs, grid_size, grid, color_amount, turns, input_file)
    solver.uninformed_method(bfs, grid_size, grid, color_amount, turns, input_file)
