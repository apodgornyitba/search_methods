# Used to implement deep-first search
class DeepFirstSearch():

    def __init__(self):
        self.frontier = []

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

    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        else:
            #first in first out
            node = self.frontier[0]
            self.frontier = self.frontier[1:]
            return node
        
class PriorityQueue(DeepFirstSearch):

    def contains_state(self, state):
        return any(node.state == state for node, _ in self.frontier)

    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        else:
            # the node with the lowest priority is the first one
            max_val = 0
            for i in range(len(self.frontier)):
                if self.frontier[i][1] < self.frontier[max_val][1]:
                    max_val = i
            node = self.frontier[max_val]
            del self.frontier[max_val]
            return node
