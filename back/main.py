from node import Node
from frontier import StackFrontier, QueueFrontier
from grid import Grid
import sys

class Game():
    def __init__(self):
        self.grid = Grid(3, ["#FF0000", "#00FF00", "#0000FF", "#FFFF00", "#FF00FF", "#00FFFF"])
        self.frontier = QueueFrontier()
        self.explored = set()
        self.solution = None


f = open("output.html", "w")

g = Game()
f.write(f'''<html>
<head>
<title>HTML File</title>
</head> 
<body>
''' + str(g.grid) + '''
</body>
</html>''')
f.close()