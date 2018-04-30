import numpy as np
from board import Board


class Node(object):
    def __init__(self, depth, player, board, value):
        self.depth = depth
        self.player = player
        self.board = board
        self.value = self.getValue(value)
        self.children = []
        self.CreateChildren()

    def getValue(self, value):
        if value:
            return value
        else:
            INIT_BEST_VAL = [+np.inf, -np.inf]
            return INIT_BEST_VAL[self.depth % 2]

    def CreateChildren(self):
        if self.depth >= 0 and not self.board.game_ended():
            for piece in self.board.pieces[self.player]:
                possible_moves = piece.possibleMoves()
                if possible_moves:
                    for move in piece.possibleMoves():
                        self.children.append(Node(self.depth - 1,
                                                  1 - self.player,  # invert between 0(black) and 1(white)
                                                  self.board.movePiece(move),
                                                  -self.value))


    def MinMax(self, node, depth_limit):
        if (depth_limit == 0) or (node.board.check_win()):
            return self.board.getE()

        # d%2 == 0 -> min's move -> +inf
        # d%2 == 1 -> max's move -> -inf
        INIT_BEST_VAL = [+np.inf, -np.inf]
        best_val = INIT_BEST_VAL[node.depth % 2]
        for child in node.children:
            val = self.MinMax(child, depth_limit - 1)
            # update best for min max
            if ((node.depth % 2 == 0) and (val < best_val)) or ((node.depth % 2 == 1) and (val > best_val)):
                best_val = val
        return best_val







