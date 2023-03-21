from config import Config
from solver import Solver
from frontier import DeepFirstSearch, BreadthFirstSearch

config = Config.parse()

solver = Solver()

for key, value in config.methods.items():
    if key == 'dfs' and value == True:
        dfs = DeepFirstSearch()
        solver.uninformed_method(dfs, config.grid_size, config.grid, config.color_amount, config.turns, config.input_file)
    if key == 'bfs' and value == True:
        bfs = BreadthFirstSearch()
        solver.uninformed_method(bfs, config.grid_size, config.grid, config.color_amount, config.turns, config.input_file)
    if key == 'greedy' and value == True:
        solver.informed_method('greedy', config.grid_size, config.grid, config.color_amount, config.turns, config.heuristic, config.input_file)
    if key == 'astar' and value == True:
        solver.informed_method('astar', config.grid_size, config.grid, config.color_amount, config.turns, config.heuristic, config.input_file)



