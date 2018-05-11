from helpers import mul2list
from copy import deepcopy

INIT_BEST_VAL = [-1000, 1000]
MAX, MIN = 0, 1


class Node(object):
    def __init__(self, depth, my_color, board, action, max_color):
        self.depth = depth
        self.my_color = my_color
        self.board = board
        self.value = None
        self.action = action
        self.children = []
        self.max_color = max_color
        self.create_children()



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
                                              move,
                                              self.max_color))

    def minmax(self, depth_limit, turns):
        if (depth_limit == 0) or (self.board.game_ended()):
            return self.get_e(turns)

        # max -> -inf
        # min -> +inf
        m = abs(self.max_color - self.my_color)
        best_val = INIT_BEST_VAL[m]

        for child in self.children:
            val = child.minmax(depth_limit - 1, turns + 1)
            # update best for min max
            if (m == MAX and (val > best_val)) or (m == MIN and (val < best_val)):
                best_val = val
        return best_val

    # Evaluation
    def get_e(self, turns):
        my_e = 0
        enemy_e = 0
        if turns == -1:
            weights = [1, 0.419951280104073,  -0.613176001482239]
        else:
            weights = [1, 0.419951280104073, 0.826045902106665, -0.246892542362536, -0.613176001482239]
        for wf in mul2list(weights, self.board.get_features(self.my_color, turns)):
            my_e += wf
        for wf in mul2list(weights, self.board.get_features(1 - self.my_color, turns)):
            enemy_e += wf
        return my_e - enemy_e
