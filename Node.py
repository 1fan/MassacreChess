from judge import *


class Node(object):
    cost = 0
    heuristic = 0
    G = cost + heuristic
    route = []
    black = []
    white = []

    def __init__(self, black, white, route, cost):
        self.route = route
        self.white = white
        self.black = black
        self.cost = cost
        self.heuristic = self.getH()
        self.G = self.heuristic + self.cost

    def __repr__(self):
        return repr((self.black, self.white, self.route, self.heuristic))

    def getH(self):
        h = 0
        b = self.black[0]  # the black piece to be eliminated
        for W in self.white:
            h += getManhattanDistance(b, W)
        return h
