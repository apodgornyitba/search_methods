from gamecolor import Color, GameColor

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

