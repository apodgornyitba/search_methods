from fill_zone import FillZone
from gamecolor import Color

class Node:
    def __init__(self, state: FillZone, parent, action: Color, cost: int = 0):
        self.state = state
        self.parent = parent
        self.action = action
        self.cost = cost
    
    def get_state(self):
        return self.state