from node import Node
from frontier import DeepFirstSearch, BreadthFirstSearch
from fill_zone import FillZone, GameStatus
from gamecolor import Color
from parserInput import Parser

import copy
import time
import sys

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

    def uninformed_method(self, algorithm: DeepFirstSearch, grid_size: int, grid, color_amount: int, turns: int):
        self.num_explored = 0

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
                raise Exception("no solution")

            # Choose a node from the frontier
            node = frontier.remove()
            self.num_explored += 1

            # If node is the goal, then we have a solution
            if node.state.game_status == GameStatus.WIN:
                actions = []
                while node.parent is not None:
                    actions.append(node.action.name)
                    node = node.parent
                actions.reverse()
                self.solution = actions
                print('Solution: {}'.format(actions))
                return

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

    start = time.time()
    solver.uninformed_method(dfs, grid_size, grid, color_amount, turns)
    end = time.time()
    print('Dfs time: {}'.format(end - start))

    start = time.time()
    solver.uninformed_method(bfs, grid_size, grid, color_amount, turns)
    end = time.time()
    print('Bfs time: {}'.format(end - start))
