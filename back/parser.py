from pydoc import doc
from gamecolor import GameColor
import sys

class Parser():

    def __init__(self):
        pass

    @staticmethod
    def parse_color_file(filename: str):
        with open(filename, 'r') as file:
            # Read in the possible colors from the first line of the file
            color_amount = int(file.readline())

            if color_amount > 6:
                print("Too many colors")
                return None
            
            # Read in the matrix of color from the remaining lines of the file
            color_matrix = []
            for line in file:
                color_matrix.append(list(map(int, line.strip().split(" "))))
                
            return (color_amount, color_matrix)
    
    @staticmethod
    def parse_solution_file(filename: str):
        with open(filename, 'r') as file:
            solution = file.readlines()
            return (len(solution), solution)

    @staticmethod
    def generate_solution_file(algorithm: str, grid, input_file: str, solution):
        if input_file is None:
            name = 'solutions/{}-sol-{}x{}'.format(algorithm, len(grid), len(grid))
        else:
            name = 'solutions/{}-sol-{}'.format(algorithm, input_file.split('\\')[-1])
        with open(name, 'w') as file:
            original_stdout = sys.stdout
            sys.stdout = file
            for i in range(len(grid)):
                for j in range(len(grid)):
                    print(GameColor(grid[i][j]).name, end=" ")
                print()
            for action in solution:
                print(action)
            sys.stdout = original_stdout
