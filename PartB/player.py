from board import Board
from node import Node
from referee import _InvalidActionException


class Player:
    # initialize: phase_turns, board, phase, color:BLACK, WHITE = 0, 1
    def __init__(self, colour):
        match_color = {'black': 0, 'white': 1}
        self.color = match_color[colour]
        self.phase = "placing"
        self.phase_turns = 0
        self.board = Board()

    def action(self, turns):
        if self.phase == "placing":
            if turns < 24:
                self.phase_turns += 1
                return self.best_place()
            elif turns == 24:
                self.phase = "moving"
                self.phase_turns = 0

        if self.phase == "moving":
            # shrink the board before my move
            if turns in [128, 196]:
                self.board.shrink_board(turns)

            # Give a best move
            best_move = self.best_move()

            # Make the move on my board
            self.board.place_piece(best_move, self.color)
            self.phase_turns += 1

            # shrink the board after my move
            turns += 1
            if turns in [128, 196]:
                self.board.shrink_board(turns)

            return best_move

    def update(self, action):
        # adjust opponent's piece
        # if action is a nested tuple --> it is a 'move'; else --> it is a 'place'
        enemy_color = 1 - self.color
        if isinstance(action[0], tuple):
            self.board.move_piece(action, enemy_color)
        elif isinstance(action[0], int):
            self.board.place_piece(action, enemy_color)
        else:
            raise _InvalidActionException

    # Make decision of move a piece
    def best_move(self):
        depth_limit = 4  # must be even number for this implementation
        root = Node(depth_limit, self.color, self.board, None)
        # d%2 == 0 -> min's move -> +inf
        # d%2 == 1 -> max's move -> -inf

        best_val = root.children[0].value
        best_move = 0
        i = 0
        for child in root.children:
            val = child.minmax(child, depth_limit - 1, self.phase_turns)
            # update best value and move for min max
            if ((child.depth % 2 == 0) and (val < best_val)) or ((child.depth % 2 == 1) and (val > best_val)):
                best_val = val
                best_move = i
        return root.children[best_move]

    # Make decision of placing a piece, call Board.placePiece() function to update the board.
    def best_place(self):
        pass
    #   return place. (,).
