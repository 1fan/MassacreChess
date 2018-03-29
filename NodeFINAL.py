from judge import *
import math


class Node(object):
    cost = 0
    huristicValue = 0
    G = cost + huristicValue
    route = []
    black = []
    white = []

    def __init__(self, black, white, route, cost):
        self.route = route
        self.white = white
        self.black = black
        self.cost = cost
        self.huristicValue = self.getH()
        self.G = self.huristicValue + self.cost

    def __repr__(self):
        return repr((self.black, self.white, self.route, self.huristicValue))

    def getH(self):
        h = 0
        b = self.black[0]  # the black piece to be eliminated
        for W in self.white:
            h += getManhattanDistance(b, W)
        return h
