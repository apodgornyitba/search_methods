from pydoc import doc
from gamecolor import Color, HexColor
import sys
import os


class Parser():

    def __init__(self):
        pass

    @classmethod
    def parse_color_file(cls, filename: str):
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
                
        return color_amount, color_matrix
    
    @classmethod
    def parse_solution_file(cls, filename: str):
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

    @classmethod
    def generate_solution_file(cls, algorithm: str, grid, input_file: str, solution):
        if input_file is None:
            filename = '{}-sol-{}x{}.txt'.format(algorithm, len(grid), len(grid))
        else:
            # Split the input file path into its directory and filename components
            _, input_file_name = os.path.split(input_file)
            # Extract the filename without the extension
            input_file_basename = os.path.splitext(input_file_name)[0]
            # Construct the output file name using the correct path separator
            filename = '{}-sol-{}.txt'.format(algorithm, input_file_basename)
        
        # Define the directory path and file name
        directory = 'solutions'

        # Create the directory if it doesn't exist
        if not os.path.exists(directory):
            os.makedirs(directory)

        with open(os.path.join(directory, filename), 'w') as file:
            for i in range(len(grid)):
                for j in range(len(grid)):
                    file.write(Color(grid[i][j]).name + " ")
                file.write("\n")
            for action in solution:
                file.write(str(action) + "\n")
