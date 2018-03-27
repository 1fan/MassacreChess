class Node(object):
    cost = 0
    huristicValue = 0
    # G = cost + huristicValue
    route = []
    black = []
    white = []

    def __init__(self, black, white, parentRoute,huristicValue):
        self.route = parentRoute
        self.huristicValue = huristicValue
        self.white = white
        self.black = black
        G = huristicValue + self.cost

    def __repr__(self):
        return repr((self.black, self.white, self.route, self.huristicValue))

