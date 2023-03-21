import json
import random
from game_parser import Parser 


def generate_random_grid(grid_size: int, color_amount: int):
    grid = []
    for i in range(grid_size):
        row = []
        for j in range(grid_size):
            row.append(random.randint(0, color_amount - 1))
        grid.append(row)
    return grid

class Config:
    def __init__(self, grid, grid_size, color_amount, turns, methods, heuristic, input_file):
        self.grid = grid
        self.grid_size = grid_size
        self.color_amount = color_amount
        self.turns = turns
        self.methods = methods
        self.heuristic = heuristic
        self.input_file = input_file

    @classmethod
    def parse(cls):
        with open('config.json', 'r') as f:
            data = json.load(f)
        
        if "file_path" in data:
            file_path = data['file_path']
            color_amount, grid = Parser.parse_color_file(file_path)
            grid_size = len(grid)
        else:
            grid = generate_random_grid(data['grid_size'], data['color_amount'])
            grid_size = data['grid_size']
            color_amount = data['color_amount']
            file_path = None

        return cls(grid, grid_size, color_amount, data['turns'], data['methods'], data['heuristic'], file_path)
    

