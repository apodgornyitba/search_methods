from gamecolor import Color, GameColor
import numpy as np

class Parser():

    def __init__(self, filename):
            
            self.filename = filename
    
            self.possible_colors = []
    
            self.color_matrix = []

    def parse_color_file(filename):
        with open(filename, 'r') as file:
            # Read in the possible colors from the first line of the file
            possible_colors = file.readline().split(" ")
            possible_colors[-1] = possible_colors[-1].split("\n")[0]   # Removing \n from last color
            for color in possible_colors:
                if color not in [e.value for e in Color]:
                    raise ValueError("Invalid color: {}".format(color))
            
            # Read in the matrix of color indices from the remaining lines of the file
            color_indices = []
            for line in file:
                color_indices.append(list(map(int, line.strip().split())))
                
            # Create the matrix of actual colors
            color_matrix = np.zeros((len(color_indices), len(color_indices[0])))
            for row in color_indices:
                color_row = np.array([])
                for index in row:
                    color_row.append(possible_colors[index])
                color_matrix.append(color_row)
                
            return color_matrix
