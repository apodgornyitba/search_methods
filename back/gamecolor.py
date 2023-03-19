from enum import IntEnum

# class GameColor(Enum):
#     CURRENT = '_'
#     PURPLE = '#ff64cc'
#     WHITE = '#ffffff'
#     RED = '#e40000'
#     GREEN = '#01e700'
#     BLUE = '#0068ff'
#     YELLOW = '#ffe700'


# class Color(Enum):
#     PURPLE = '#ff64cc'
#     WHITE = '#ffffff'
#     RED = '#e40000'
#     GREEN = '#01e700'
#     BLUE = '#0068ff'
#     YELLOW = '#ffe700'

class GameColor(IntEnum):
    CURRENT = -1
    PURPLE = 0
    WHITE = 1
    RED = 2
    GREEN = 3
    BLUE = 4
    YELLOW = 5


class Color(IntEnum):
    PURPLE = 0
    WHITE = 1
    RED = 2
    GREEN = 3
    BLUE = 4
    YELLOW = 5
