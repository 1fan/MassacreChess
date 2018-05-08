from judge import *
from copy import deepcopy

class Node(object):
    def __init__(self, depth, my_color, board, value, action):
        self.depth = depth
        self.my_color = my_color
        self.board = board
        self.value = self.get_value(value)
        self.action = action
        self.children = []
        self.create_children()

    def get_value(self, value):
        if value:
            return value
        else:
            return INIT_BEST_VAL[self.depth % 2]

    def create_children(self):
        if self.depth > 0 and not self.board.game_ended():
            possible_moves = self.board.possible_moves(self.my_color)
            if possible_moves:
                for move in possible_moves:
                    child_board = deepcopy(self.board)
                    child_board.move_piece(move, self.my_color)
                    self.children.append(Node(self.depth - 1,
                                              1 - self.my_color,  # invert between 0(black) and 1(white)
                                              child_board,
                                              (-1) * self.value,
                                              move))

    def minmax(self, node, depth_limit, turns):
        if (depth_limit == 0) or (node.board.game_ended()):
            return node.get_e(turns)

        # d%2 == 0 -> max -> -inf
        # d%2 == 1 -> min -> +inf
        best_val = INIT_BEST_VAL[node.depth % 2]
        for child in node.children:
            val = self.minmax(child, depth_limit - 1, turns)
            # update best for min max
            if ((node.depth % 2 == 0) and (val > best_val)) or ((node.depth % 2 == 1) and (val < best_val)):
                best_val = val
        return best_val

    # Evaluation
    def get_e(self, turns):
        my_e = 0
        enemy_e = 0
        if turns == -1:
            weights = [1, 0.5, 0.5]
        else:
            weights = [1, 0.5, 0.5, 0.2, 0.5]
        for wf in mul2list(weights, self.board.get_features(self.my_color, turns)):
            my_e += wf
        for wf in mul2list(weights, self.board.get_features(1 - self.my_color, turns)):
            enemy_e += wf
        return my_e - enemy_e
