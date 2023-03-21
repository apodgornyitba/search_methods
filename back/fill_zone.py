from enum import IntEnum
from random import randint
from collections import deque
from gamecolor import GameColor, Color

import copy

# from TP1.back.node import Grid
class Direction(IntEnum):
    TOP = 1
    BOTTOM = 2
    RIGHT = 3
    LEFT = 4

class Cell:
    def __init__(self, x: int, y: int, dir_from: Direction):
        self.x = x
        self.y = y
        self.dir_from = dir_from

class GameStatus:
    CONTINUES = 1
    WIN = 2
    LOSS = 3

class FillZone:

    def __init__(self, grid_size: int, grid, color_amount: int, turns: int, current_color = None):
        self.__grid_size = grid_size
        self.__color_amount = color_amount
        self.__frontier_queue = deque()
        self.turns = turns
        self.game_colors = [e for e in Color]

        self.remaining_cells = grid_size * grid_size - 1            # Initial cell is always colored
        self.game_status = GameStatus.CONTINUES
        self.__setup_game(grid, grid[0][0] if current_color is None else current_color)
    
    def __deepcopy__(self, memodict={}):
        cpy_obj = type(self)(self.__grid_size, copy.deepcopy(self.grid), self.__color_amount, self.turns, self.current_color)

        cpy_obj.remaining_cells = self.remaining_cells
        cpy_obj.game_status = self.game_status
        cpy_obj.__frontier_queue = copy.deepcopy(self.__frontier_queue)

        return cpy_obj

    def __setup_game(self, grid, current_color):
        self.grid = grid
        self.current_color = current_color
        self.grid[0][0] = GameColor.CURRENT
        self.__expand_frontier(0, 0, Direction.TOP)
    
    # Returns GameStatus after move
    def change_color(self, new_color: Color):
        self.current_color = new_color
        #print('Changing color to {}'.format(new_color.value))

        frontier_size = len(self.__frontier_queue)
        for i in range(frontier_size):
            cell = self.__frontier_queue.pop()
            self.__expand_frontier(cell.x, cell.y, cell.dir_from)
        
        if self.remaining_cells <= 0:       # TODO: Check it stops at zero
            # print('You won')
            self.game_status = GameStatus.WIN
        
        if self.turns <= 0:
            # print('You lost')
            self.game_status = GameStatus.LOSS
        
        self.turns = self.turns - 1
        # print('Remaining turns: {}'.format(self.turns))
        # print('Remaining cells: {}'.format(self.remaining_cells))
        # print('Frontier cells: {}'.format(self.__frontier_queue.qsize()))
        #for cell in self.__frontier_queue:
        #    print('- x: {}, y: {}, from: {}'.format(cell.x, cell.y, cell.dir_from.name))
        #print(self.grid)
        return self.game_status

    def __is_frontier(self, x: int, y: int):
        if x>0 and GameColor.CURRENT != self.grid[x - 1][y]:
            return True
        if x+1 < self.__grid_size and GameColor.CURRENT != self.grid[x + 1][y]:
            return True
        if y>0 and GameColor.CURRENT != self.grid[x][y - 1]:
            return True
        if y+1 < self.__grid_size and GameColor.CURRENT != self.grid[x][y + 1]:
            return True
        return False
    
    # x.y
    # 0.0 0.1 0.2
    # 1.0 1.1 1.2
    # 2.0 2.1 2.2
    def __expand_frontier(self, x: int, y: int, dir_from: Direction):
        # Calculate if expansion is needed and do recursively
        if x+1 < self.__grid_size and self.current_color == self.grid[x+1][y] and dir_from != Direction.BOTTOM:
            self.grid[x+1][y] = GameColor.CURRENT
            self.remaining_cells = self.remaining_cells - 1
            self.__expand_frontier(x+1, y, Direction.TOP)
        if x>0 and self.current_color == self.grid[x-1][y] and dir_from != Direction.TOP:
            self.grid[x-1][y] = GameColor.CURRENT
            self.remaining_cells = self.remaining_cells - 1
            self.__expand_frontier(x-1, y, Direction.BOTTOM)
        if y+1 < self.__grid_size and self.current_color == self.grid[x][y+1] and dir_from != Direction.RIGHT:
            self.grid[x][y+1] = GameColor.CURRENT
            self.remaining_cells = self.remaining_cells - 1
            self.__expand_frontier(x, y+1, Direction.LEFT)
        if y>0 and self.current_color == self.grid[x][y-1] and dir_from != Direction.LEFT:
            # raise Exception('current is {} and prev is {}'.format(self.current_color, self.grid[x][y-1]))
            self.grid[x][y-1] = GameColor.CURRENT
            self.remaining_cells = self.remaining_cells - 1
            self.__expand_frontier(x, y-1, Direction.RIGHT)

        # Recalculate frontier after expansion finished
        if self.__is_frontier(x, y):
            self.__frontier_queue.appendleft(Cell(x, y, dir_from))

    def __eq__(self, obj):
        if not isinstance(obj, FillZone):
            return False
        if self.current_color != obj.current_color:
            return False
        for x in range(self.__grid_size):
            for y in range(self.__grid_size):
                if self.grid[x][y] != obj.grid[x][y]:
                    return False
        return True
    
    def __neq__(self, obj):
        return not obj == self

    def __hash__(self) -> int:
        return hash(tuple(tuple(row) for row in self.grid))
