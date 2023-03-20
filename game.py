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
import arcade
import arcade.gui
import sys

from back.gamecolor import GameColor
from back.fill_zone import FillZone
from back.parser import Parser

# N: Number of rows and columns
# M: Number of colors available
N = 10
M = 5

# WHITE, RED, GREEN, BLUE, YELLOW
COLORS = ['#ff64cc', '#ffffff', '#e40000', '#01e700', '#0068ff', '#ffe700']

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

    def __init__(self, input_file: str, solution_file: str): #, width, height, title):
        """
        Set up the application.
        """
        parser = Parser()
        (self.color_amount, self.grid) = parser.parse_color_file(input_file)
        self.grid_size = len(self.grid)
        (self.turns, self.solution) = parser.parse_solution_file(solution_file)

        self.grid = FillZone(self.grid_size, self.grid, self.color_amount, )

        self.screen_width = (WIDTH + MARGIN) * self.grid_size + MARGIN
        self.screen_height = (HEIGHT + MARGIN) * self.grid_size + MARGIN

        super().__init__(self.screen_width, self.screen_height, SCREEN_TITLE)

        # Set the background color of the window
        self.background_color = arcade.color.BLACK

        # One dimensional list of all sprites in the two-dimensional sprite list
        self.color_sprite_list = arcade.SpriteList()

        i = 0
        for color in COLORS:
            sprite = arcade.SpriteSolidColor(WIDTH, HEIGHT, arcade.color_from_hex_string(color))
            sprite.center_x = 25 + i * (WIDTH + 10)
            sprite.center_y = self.screen_height - 25
            self.color_sprite_list.append(sprite)
            i += 1

        # TODO: Add shuffle button
        self.shuffle_button = arcade.gui.UIFlatButton(text='Shuffle')
        
        self.button_container = arcade.gui.UIBoxLayout()
        self.button_container.add(self.shuffle_button)

        # One dimensional list of all sprites in the two-dimensional sprite list
        self.grid_sprite_list = arcade.SpriteList()

        # This will be a two-dimensional grid of sprites to mirror the two
        # dimensional grid of numbers. This points to the SAME sprites that are
        # in grid_sprite_list, just in a 2d manner.
        self.grid_sprites = []

        # Create a list of solid-color sprites to represent each grid location
        for row in range(ROW_COUNT):
            self.grid_sprites.append([])
            for column in range(COLUMN_COUNT):
                x = column * (WIDTH + MARGIN) + (WIDTH / 2 + MARGIN)
                y = row * (HEIGHT + MARGIN) + (HEIGHT / 2 + MARGIN)
                sprite = arcade.SpriteSolidColor(WIDTH, HEIGHT, arcade.color.WHITE)
                sprite.center_x = x
                sprite.center_y = y
                self.grid_sprite_list.append(sprite)
                self.grid_sprites[row].append(sprite)
        
        arcade.schedule(function_pointer=self.do_movement, interval=1)

    # TODO: Process game movements here
    def do_movement(self, delta_time):
        # Flip the color of the sprite
        if self.grid_sprites[0][0].color == arcade.color.WHITE:
            self.grid_sprites[0][0].color = arcade.color.BLUE
        else:
            self.grid_sprites[0][0].color = arcade.color.WHITE

    def on_draw(self):
        """
        Render the screen.
        """

        self.manager = arcade.gui.UIManager()
        self.manager.enable()

        # We should always start by clearing the window pixels
        self.clear()

        self.color_sprite_list.draw()

        # Create a widget to hold the v_box widget, that will center the buttons
        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="right",
                anchor_y="top",
                child=self.button_container)
        )

        self.manager.draw()

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
        if self.grid_sprites[row][column].color == arcade.color.WHITE:
            self.grid_sprites[row][column].color = arcade.color.GREEN
        else:
            self.grid_sprites[row][column].color = arcade.color.WHITE


def main():
    n = sys.argv
    if n != 2:
        raise Exception('Must provide both input grid and solution files')
    input_file = sys.argv[0]
    solution_file = sys.argv[1]
    MyGame(input_file, solution_file)
    arcade.run()


if __name__ == "__main__":
    main()