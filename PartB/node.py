from judge import *


class Node(object):
    def __init__(self, depth, my_color, board, value):
        self.depth = depth
        self.my_color = my_color
        self.board = board
        self.value = self.get_value(value)
        self.children = []
        self.create_children()

    def get_value(self, value):
        if value:
            return value
        else:
            return INIT_BEST_VAL[self.depth % 2]

    def create_children(self):
        if self.depth > 0 and not self.board.game_ended():
            for piece in self.board.Pieces[self.my_color]:
                possible_moves = piece.possible_moves()
                if possible_moves:
                    for move in possible_moves:
                        self.children.append(Node(self.depth - 1,
                                                  1 - self.my_color,  # invert between 0(black) and 1(white)
                                                  self.board.move_piece(move, self.my_color),
                                                  (-1)*self.value))

    def minmax(self, node, depth_limit, turns):
        if (depth_limit == 0) or (node.board.check_win()):
            return self.get_e(turns)

        # d%2 == 0 -> min's move -> +inf
        # d%2 == 1 -> max's move -> -inf
        best_val = INIT_BEST_VAL[node.depth % 2]
        for child in node.children:
            val = self.minmax(child, depth_limit - 1, turns)
            # update best for min max
            if ((node.depth % 2 == 0) and (val < best_val)) or ((node.depth % 2 == 1) and (val > best_val)):
                best_val = val
        return best_val

    # Evaluation
    def get_e(self, turns):
        my_e = 0
        enemy_e = 0
        for wf in mul2list(self.board.weights, self.board.get_features(self.my_color, turns)):
            my_e += wf
        for wf in mul2list(self.board.weights, self.board.get_features(1 - self.my_color, turns)):
            enemy_e += wf
        return my_e - enemy_e
