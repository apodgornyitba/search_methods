# Used to implement deep-first search
class DeepFirstSearch():

    def __init__(self):
        self.frontier = []
        self.name = 'DFS'

    def add(self, node):
        self.frontier.append(node)

    def contains_state(self, state):
        return any(node.state == state for node in self.frontier)

    def empty(self):
        return len(self.frontier) == 0

    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        else:
            #last in first out
            node = self.frontier[-1]
            self.frontier = self.frontier[:-1]  
            return node

# Used to implement breadth-first search
class BreadthFirstSearch(DeepFirstSearch):

    def __init__(self):
        super().__init__()
        self.name = 'BFS'

    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        else:
            #first in first out
            node = self.frontier[0]
            self.frontier = self.frontier[1:]
            return node