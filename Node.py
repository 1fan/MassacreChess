from judge import *
class Node(object):
    cost = 0
    huristicValue = 0
    G = cost + huristicValue
    route = []
    black = []
    white = []

    def __init__(self, black, white, route, cost):
        self.route = route
        self.huristicValue = 0
        self.white = white
        self.black = black
        self.cost = cost
        G = self.huristicValue + self.cost

    def __repr__(self):
        return repr((self.black, self.white, self.route, self.huristicValue))

    def getH(self):
        H = []  # stores h_up&down and h_left&right
        black = self.black[0]  # the black piece to be eliminated
        for twoD in [[(0, -1), (0, +1)], [(-1, 0), (+1, 0)]]:
            h = 0  # sum of the two distances from the two opposite neighbors to their closest white piece
            for oneD in twoD:
                c_to = neighborOf(black, oneD)
                c_from = findNearstWhite(self, c_to)
                h += getManhattanDistance(c_from, c_to)
            H.append(h)
        self.huristicValue = min(H)