from enum import Enum, IntEnum
from random import randint
import queue
import timeit

class Color(Enum):
    CURRENT = '_'
    PURPLE = '#ff64cc'
    WHITE = '#ffffff'
    RED = '#e40000'
    GREEN = '#01e700'
    BLUE = '#0068ff'
    YELLOW = '#ffe700'

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
    def __init__(self, grid_size: int, color_amount: int, limit_turns: int):
        self.__grid_size = grid_size
        self.__color_amount = color_amount
        self.__frontier_queue = queue.Queue()

        self.turns = limit_turns
        self.game_colors = [e.value for e in Color]
        self.remaining_cells = grid_size * grid_size - 1            # Initial cell is always colored

        self.__setup_game()

    # Sets up the grid
    def __setup_game(self):
        for x in range(self.__grid_size):
            if x == 0:
                self.grid = [None] * self.__grid_size
            for y in range(self.__grid_size):
                if y == 0:
                    self.grid[x] = [None] * self.__grid_size
                self.grid[x][y] = self.game_colors[randint(1, self.__color_amount)]
        self.current_color = self.grid[0][0]
        print('Inicio con color {}'.format(self.grid[0][0]))
        print(self.grid)
        self.grid[0][0] = Color.CURRENT.value
        self.__expand_frontier(0, 0, Direction.TOP)
    
    # Returns GameStatus after move
    def change_color(self, new_color: Color):
        self.current_color = new_color

        frontier_size = self.__frontier_queue.qsize()
        for i in range(frontier_size):
            cell = self.__frontier_queue.get()
            self.__expand_frontier(cell.x, cell.y, cell.dir_from)
        
        if self.remaining_cells <= 0:       # TODO: Check it stops at zero
            print('You won')
            return GameStatus.WIN
        
        if self.turns == 0:
            print('You lost')
            return GameStatus.LOSS
        
        self.turns = self.turns - 1
        print('Remaining turns: {}'.format(self.turns))
        print('Remaining cells: {}'.format(self.remaining_cells))
        print('Frontier cells: {}'.format(self.__frontier_queue.qsize()))
        #for cell in self.__frontier_queue:
        #    print('- x: {}, y: {}, from: {}'.format(cell.x, cell.y, cell.dir_from.name))
        print(self.grid)
        print()
        return GameStatus.CONTINUES

    def __is_frontier(self, x: int, y: int):
        if x>0 and Color.CURRENT.value != self.grid[x-1][y]:
            return True
        if x+1 < self.__grid_size and Color.CURRENT.value != self.grid[x+1][y]:
            return True
        if y>0 and Color.CURRENT.value != self.grid[x][y-1]:
            return True
        if y+1 < self.__grid_size and Color.CURRENT.value != self.grid[x][y+1]:
            return True
        return False
    
    # x.y
    # 0.0 0.1 0.2
    # 1.0 1.1 1.2
    # 2.0 2.1 2.2
    def __expand_frontier(self, x: int, y: int, dir_from: Direction):
        # Calculate if expansion is needed and do recursively
        if x+1 < self.__grid_size and self.current_color == self.grid[x+1][y] and dir_from != Direction.BOTTOM:
            self.grid[x+1][y] = Color.CURRENT.value
            self.remaining_cells = self.remaining_cells - 1
            self.__expand_frontier(x+1, y, Direction.TOP)
        if x>0 and self.current_color == self.grid[x-1][y] and dir_from != Direction.TOP:
            self.grid[x-1][y] = Color.CURRENT.value
            self.remaining_cells = self.remaining_cells - 1
            self.__expand_frontier(x-1, y, Direction.BOTTOM)
        if y+1 < self.__grid_size and self.current_color == self.grid[x][y+1] and dir_from != Direction.RIGHT:
            self.grid[x][y+1] = Color.CURRENT.value
            self.remaining_cells = self.remaining_cells - 1
            self.__expand_frontier(x, y+1, Direction.LEFT)
        if y>0 and self.current_color == self.grid[x][y-1] and dir_from != Direction.LEFT:
            self.grid[x][y-1] = Color.CURRENT.value
            self.remaining_cells = self.remaining_cells - 1
            self.__expand_frontier(x, y-1, Direction.RIGHT)

        # Recalculate frontier after expansion finished
        if self.__is_frontier(x, y):
            self.__frontier_queue.put(Cell(x, y, dir_from))


def main():
    grid_size = 14
    color_amount = 3
    turns = 30

    game = FillZone(grid_size, color_amount, turns)
    game_colors = game.game_colors
    start = timeit.timeit()
    for i in range(turns):
        new_color = game_colors[randint(1, color_amount)]
        print('Changing color to {}'.format(new_color))
        game.change_color(new_color)
    end = timeit.timeit()
    print(end - start)

if __name__ == "__main__":
    main()