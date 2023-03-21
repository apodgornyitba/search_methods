"""
Array Backed Grid Shown By Sprites

Show how to use a two-dimensional list/array to back the display of a
grid on-screen.

This version makes a grid of sprites instead of numbers. Instead of
interating all the cells when the grid changes we simply just
swap the color of the selected sprite. This means this version
can handle very large grids and still have the same performance.

If Python and Arcade are installed, this example can be run from the command line with:
python -m arcade.examples.array_backed_grid_sprites_2
"""
from fill_zone import GameStatus
from gamecolor import HexColor
import arcade
import arcade.gui
import sys

from gamecolor import GameColor, Color
from fill_zone import FillZone
from game_parser import Parser

# N: Number of rows and columns
# M: Number of colors available
N = 10
M = 5

# Set how many rows and columns we will have
ROW_COUNT = N
COLUMN_COUNT = N

# This sets the WIDTH and HEIGHT of each grid location
WIDTH = 30
HEIGHT = 30

# This sets the margin between each cell
# and on the edges of the screen.
MARGIN = 5

# Do the math to figure out our screen dimensions
# SCREEN_WIDTH = (WIDTH + MARGIN) * COLUMN_COUNT + MARGIN
# SCREEN_HEIGHT = (HEIGHT + MARGIN) * ROW_COUNT + MARGIN + 50
SCREEN_TITLE = "Fill-Zone game"

class MyGame(arcade.Window):
    """
    Main application class.
    """

    def __init__(self, solution_file: str): #, width, height, title):
        """
        Set up the application.
        """
        parser = Parser()
        self.colors = [c.value for c in HexColor]
        #self.colors = [arcade.color.PURPLE, arcade.color.WHITE, arcade.color.RED, arcade.color.GREEN, arcade.color.BLUE, arcade.color.YELLOW]
        # print(self.colors)
        (self.grid, self.color_amount, self.solution) = parser.parse_solution_file(solution_file)
        self.turns = len(self.solution)
        self.grid_size = len(self.grid)

        self.fillzone = FillZone(self.grid_size, self.grid, self.color_amount, self.turns)

        self.screen_width = (WIDTH + MARGIN) * self.grid_size + MARGIN
        self.screen_height = (HEIGHT + MARGIN) * self.grid_size + MARGIN

        super().__init__(self.screen_width, self.screen_height, SCREEN_TITLE)

        # Set the background color of the window
        self.background_color = arcade.color.BLACK

        # One dimensional list of all sprites in the two-dimensional sprite list
        self.color_sprite_list = arcade.SpriteList()

        # Counter for current action
        self.current_action = 0

        #i = 0
        #for color in COLORS:
        #    sprite = arcade.SpriteSolidColor(WIDTH, HEIGHT, arcade.color_from_hex_string(color))
        #    sprite.center_x = 25 + i * (WIDTH + 10)
        #    sprite.center_y = self.screen_height - 25
        #    self.color_sprite_list.append(sprite)
        #    i += 1

        # TODO: Add shuffle button
        #self.shuffle_button = arcade.gui.UIFlatButton(text='Shuffle')
        
        #self.button_container = arcade.gui.UIBoxLayout()
        #self.button_container.add(self.shuffle_button)

        # One dimensional list of all sprites in the two-dimensional sprite list
        self.grid_sprite_list = arcade.SpriteList()

        # This will be a two-dimensional grid of sprites to mirror the two
        # dimensional grid of numbers. This points to the SAME sprites that are
        # in grid_sprite_list, just in a 2d manner.
        self.grid_sprites = []

        # Create a list of solid-color sprites to represent each grid location
        for row in range(self.grid_size):
            self.grid_sprites.append([])
            for column in range(self.grid_size):
                x = column * (WIDTH + MARGIN) + (WIDTH / 2 + MARGIN)
                y = self.screen_height - (row * (HEIGHT + MARGIN) + (HEIGHT / 2 + MARGIN))
                #sprite = arcade.SpriteSolidColor(WIDTH, HEIGHT, arcade.color.WHITE)
                sprite = arcade.SpriteSolidColor(WIDTH, HEIGHT, arcade.color_from_hex_string(self.colors[self.grid[row][column]]))
                sprite.center_x = x
                sprite.center_y = y
                self.grid_sprite_list.append(sprite)
                self.grid_sprites[row].append(sprite)
        
        arcade.schedule(function_pointer=self.do_movement, interval=2)

    # TODO: Process game movements here
    def do_movement(self, delta_time):
        if self.fillzone.game_status == GameStatus.CONTINUES:
            new_color = self.solution[self.current_action]
            self.fillzone.change_color(Color[new_color])

            for row in range(self.grid_size):
                for column in range(self.grid_size):
                    old_sprite = self.grid_sprites[row][column]
                    x = column * (WIDTH + MARGIN) + (WIDTH / 2 + MARGIN)
                    y = self.screen_height - (row * (HEIGHT + MARGIN) + (HEIGHT / 2 + MARGIN))
                    #sprite = arcade.SpriteSolidColor(WIDTH, HEIGHT, arcade.color.WHITE)

                    sprite_color = arcade.color_from_hex_string(self.colors[self.fillzone.current_color])
                    if self.fillzone.grid[row][column] != GameColor.CURRENT:
                        sprite_color = arcade.color_from_hex_string(self.colors[self.fillzone.grid[row][column]])

                    sprite = arcade.SpriteSolidColor(WIDTH, HEIGHT, sprite_color)
                    sprite.center_x = x
                    sprite.center_y = y
                    old_sprite.remove_from_sprite_lists()
                    self.grid_sprite_list.append(sprite)
                    self.grid_sprites[row].append(sprite)
            # Flip the color of the sprite
            #for x in range(self.grid_size):
            #    for y in range(self.grid_size):
            #        old_sprite = self.grid_sprites[x][y]
            #        self.grid_sprites[x][y] = arcade.SpriteSolidColor(WIDTH, HEIGHT, arcade.color_from_hex_string(self.game_grid[row][column]))
            #        self.grid_sprites[x][y].color = arcade.color_from_hex_string(self.colors[self.fillzone.current_color])
            #        if self.fillzone.grid[x][y] != GameColor.CURRENT:
            #            self.grid_sprites[x][y].color = arcade.color_from_hex_string(self.colors[self.fillzone.grid[x][y]])
            self.current_action = self.current_action + 1

    def on_draw(self):
        """
        Render the screen.
        """

        # We should always start by clearing the window pixels
        self.clear()

        # Create a widget to hold the v_box widget, that will center the buttons

        # Batch draw the grid sprites
        self.grid_sprite_list.draw()

    def on_mouse_press(self, x, y, button, modifiers):
        """
        Called when the user presses a mouse button.
        """

        # Convert the clicked mouse position into grid coordinates
        column = int(x // (WIDTH + MARGIN))
        row = int(y // (HEIGHT + MARGIN))

        print(f"Click coordinates: ({x}, {y}). Grid coordinates: ({row}, {column})")

        # Make sure we are on-grid. It is possible to click in the upper right
        # corner in the margin and go to a grid location that doesn't exist
        if row >= ROW_COUNT or column >= COLUMN_COUNT:
            # Simply return from this method since nothing needs updating
            return

        # Flip the color of the sprite
        if self.grid_sprites[row][column].color == arcade.color.BLUE:
            self.grid_sprites[row][column].color = arcade.color.RED
        else:
            self.grid_sprites[row][column].color = arcade.color.RED


def main():
    n = len(sys.argv)
    if n != 2:
        raise Exception('Must provide solution file')
    solution_file = sys.argv[1]
    MyGame(solution_file)
    arcade.run()


if __name__ == "__main__":
    main()