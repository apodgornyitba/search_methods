from node import Node
from frontier import DeepFirstSearch
from fill_zone import FillZone
from color import Color
import copy

class Solver:
    def __init__(self):
        pass

    def main(self):
        grid_size = 9
        color_amount = 5
        turns = 30
        self.num_explored = 0
        self.goal = None

        start = Node(state=FillZone(grid_size, color_amount, turns), parent=None, action=None)
        frontier = DeepFirstSearch()
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
            if node.state == self.goal:
                actions = []
                cells = []
                while node.parent is not None:
                    actions.append(node.action)
                    cells.append(node.state)
                    node = node.parent
                actions.reverse()
                cells.reverse()
                self.solution = (actions, cells)
                return

            # Mark node as explored
            self.explored.add(node.state)

            # Add neighbors to frontier
            for color in Color:
                if color != node.state.current_color and not frontier.contains_state(node.state) and node.state not in self.explored:
                    print('Agrego un nodo con color {}'.format(color.name))
                    child = Node(state=copy.deepcopy(node.state), parent=node, action=color)
                    frontier.add(child)

if __name__ == "__main__":
    solver = Solver()
    solver.main()
