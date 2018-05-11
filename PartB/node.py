from helpers import mul2list
from copy import deepcopy

INIT_BEST_VAL = [-100, 100]
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
        # Return evaluation value when reach the end of tree or the game ends
        if (depth_limit == 0) or (self.board.game_ended()):
            return self.get_e(turns)

        # max if m==0, min if m==1
        m = abs(self.max_color - self.my_color)
        best_val = INIT_BEST_VAL[m]
        # Get the value for each child
        for child in self.children:
            val = child.minmax(depth_limit - 1, turns + 1)
            # update best value for min max
            if (m == MAX and (val > best_val)) or (m == MIN and (val < best_val)):
                best_val = val
        return best_val

    # Return the evaluation value of a node
    # Specify the weight HERE
    def get_e(self, turns):
        my_e = 0
        enemy_e = 0
        # Placing phase
        if turns == -1:
            weights = [1, 0.419951280104073,  -0.613176001482239]
        # Moving phase
        else:
            weights = [1, 0.419951280104073, 0.826045902106665, -0.246892542362536, -0.613176001482239]

        # Summing up the product of feature and its weight
        for wf in mul2list(weights, self.board.get_features(self.my_color, turns)):
            my_e += wf
        for wf in mul2list(weights, self.board.get_features(1 - self.my_color, turns)):
            enemy_e += wf
        return my_e - enemy_e
