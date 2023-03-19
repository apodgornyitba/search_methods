class Grid:
    def __init__(self, size: int, colors):
        self.__size = size
        self.__colors = colors

class Node:
    def __init__(self, state, parent, action):
        self.state = state
        self.parent = parent
        self.action = action
