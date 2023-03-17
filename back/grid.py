import random

class Grid():
    def __init__(self, M, colors):
        self.M = M
        self.colors = colors
        self.grid = [[0 for i in range(M)] for j in range(M)]

        # generate the grid with random colors
        for i in range(M):
            for j in range(M):
                self.grid[i][j] = random.choice(colors)

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
