from pydoc import doc
from gamecolor import Color, HexColor
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
            grid = []
            solution = []
            color_amount = set()
            line = file.readline().split(" ")
            while len(line) > 1:
                line = line[:-1]
                colors = list(map(lambda x: Color.__members__[x].value, line))
                grid.append(colors)
                for color in colors:
                    color_amount.add(color)
                line = file.readline().split(" ")
            line = line[0]
            while line != "":
                solution.append(line.split('\n')[0])
                line = file.readline()
            return (grid, len(color_amount), solution)

    @staticmethod
    def generate_solution_file(algorithm: str, grid, input_file: str, solution):
        if input_file is None:
            name = 'solutions/{}-sol-{}x{}.txt'.format(algorithm, len(grid), len(grid))
        else:
            name = 'solutions/{}-sol-{}'.format(algorithm, input_file.split('/')[-1].split('\\')[-1])
        with open(name, 'w') as file:
            original_stdout = sys.stdout
            sys.stdout = file
            for i in range(len(grid)):
                for j in range(len(grid)):
                    print(Color(grid[i][j]).name, end=" ")
                print()
            for action in solution:
                print(action)
            sys.stdout = original_stdout
