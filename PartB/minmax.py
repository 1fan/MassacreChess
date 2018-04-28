import numpy as np
BLACK, WHITE = 0, 1


class Piece:
    '''
    Return ((this pos),(next pos))
    '''
    def possible_moves(self):
        pass


class Board:
    black_pieces = []
    white_pieces = []
    pieces = [black_pieces, white_pieces]

    def make_move(self, move): # move = ((old, old),(new, new))
        pass

    def check_win(self):
        pass

    def get_e(self):
        pass

class Node(object):
    def __init__(self, depth, player, board, value = 0):
        self.depth = depth
        self.player = player
        self.board = board
        self.value = value
        self.children = []
        self.CreateChildren()

    def CreateChildren(self):
        if self.depth >= 0:
            for piece in self.board.pieces[self.player]:
                for move in piece.possible_moves():
                    self.children.append(Node(self.depth - 1,
                                              1 - self.player,  # invert between 0(black) and 1(white)
                                              self.board.make_move(move),
                                              unknown))


def MinMax(node, depth_limit):
    if (depth_limit == 0) or (node.board.check_win()):
        return self.board.get_e()

    # d%2 == 0 -> min's move -> +inf
    # d%2 == 1 -> max's move -> -inf
    INIT_BEST_VAL = [+np.inf, -np.inf]
    best_val = INIT_BEST_VAL[node.depth % 2]
    for child in node.children:
        val = MinMax(child, depth_limit - 1)
        # update best for min max
        if ((node.depth % 2 == 0) and (val < best_val)) or ((node.depth % 2 == 1) and (val > best_val)):
            best_val = val
    return best_val


class Player(object):
    def best_move(self, board, my_color):
        depth_limit = 4 # must be even number for this implementation
        root = Node(depth_limit, my_color, board, None)
        # d%2 == 0 -> min's move -> +inf
        # d%2 == 1 -> max's move -> -inf
        INIT_BEST_VAL = [+np.inf, -np.inf]
        best_val = INIT_BEST_VAL[node.depth % 2]
        best_move = 0
        i = 0
        for child in root.children:
            val = MinMax(child, depth_limit - 1)
            # update best value and move for min max
            if ((node.depth % 2 == 0) and (val < best_val)) or ((node.depth % 2 == 1) and (val > best_val)):
                best_val = val
                best_move = i
        return root.children[best_move]




