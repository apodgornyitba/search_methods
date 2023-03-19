import random

class Grid():
    def __init__(self, BOARD_SIZE, colors):
        self.BOARD_SIZE = BOARD_SIZE
        self.colors = colors
        self.grid = [[0 for i in range(BOARD_SIZE)] for j in range(BOARD_SIZE)]

        # generate the grid with random colors
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                self.grid[i][j] = random.choice(colors)

    def check_win(self):
        player_color = self.grid[0][0]
        for i in range(self.M):
            for j in range(self.M):
                if self.grid[i][j] != player_color:
                    return False
        return True

    def fill_zone(self, row, col, color, new_color):
        # Recursive function to fill all adjacent cells of the same color
        if row < 0 or row >= self.BOARD_SIZE or col < 0 or col >= self.BOARD_SIZE:
            # Return if cell is out of bounds
            return
        if self.grid[row][col] == color:
            self.grid[row][col] = new_color
            return
        if self.grid[row][col] == new_color:
            return
        
        self.grid[row][col] = [color, ]
        self.fill_zone(self, row+1, col, color, new_color)
        self.fill_zone(self, row-1, col, color, new_color)
        self.fill_zone(self, row, col+1, color, new_color)
        self.fill_zone(self, row, col-1, color, new_color)
    

    def __str__(self):
        # print the grid in html format
        table =""
        for i in range(self.M):
            for j in range(self.M):
                # print the cell with the chosen color
                table += f'<td style="background-color: {self.grid[i][j]}; width: 50px; height: 50px;"></td>'
            # start a new row
            table += "<tr>"
        # create the complete HTML document with the table in the body
        html = f'''
            <!DOCTYPE html>
            <html>
                <head>
                    <title>My HTML Document</title>
                </head>
                <body>
                    <table>
                        {table}
                    </table>
                </body>
            </html>
        '''
        return html
