from judge import *

# Node class defines the coordinates of white side and the black side using the list black and white.


class Node(object):
    cost = 0
    heuristic = 0
    f = cost + heuristic
    route = []
    black = []
    white = []

    def __init__(self, black, white, route, cost):
        self.route = route
        self.white = white
        self.black = black
        self.cost = cost
        self.heuristic = self.get_h()
        self.f = self.heuristic + self.cost

    def __repr__(self):
        return repr((self.black, self.white, self.route, self.heuristic))

    # The heuristic method to calculate the heuristic value which equals
    # the total manhattan distance between all white pieces to the target black piece.
    def get_h(self):
        h = 0
        b = self.black[0]  # the black piece to be eliminated
        for W in self.white:
            h += get_manhattan_distance(b, W)
        return h
