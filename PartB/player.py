from board import Board
from piece import Piece
from node import Node
import numpy as np
from referee import _InvalidActionException


class player:
    # initialize: turns, board, phase, color:BLACK, WHITE = 0, 1
    def __init__(self, colour):
        match_color = {'black': 0, 'white': 1}
        self.color = match_color[colour]
        self.turns = 0
        self.phase = "placing"
        self.board = Board

    def action(self, turns):
        if self.phase == "placing":
            if turns < 24:
                self.makePlace()
                self.turns += 1
            elif turns == 24:
                self.phase == "moving"
                self.turns = 0
                self.makeMove()
                self.turns += 1
        if self.phase == "moving":
            if turns in [128,196]:
                Board.shrinkBoard(turns)
            self.makeMove()
            self.turns += 1

    def update(self, action):
        # if action is a nested tuple --> it is a 'move'; else --> it is a 'place'
        if isinstance(action[0], tuple):
            self.board.movePiece(action)
        elif isinstance(action[0], int):
            self.board.placePiece(action)
        else:
            raise _InvalidActionException

    # Make decision of move a piece
    def makeMove(self):
        depth_limit = 4  # must be even number for this implementation
        root = Node(depth_limit, self.color, self.board, None)
        # d%2 == 0 -> min's move -> +inf
        # d%2 == 1 -> max's move -> -inf

        best_val = root.children[0].value
        best_move = 0
        i = 0
        for child in root.children:
            val = child.MinMax(child, depth_limit - 1)
            # update best value and move for min max
            if ((child.depth % 2 == 0) and (val < best_val)) or ((child.depth % 2 == 1) and (val > best_val)):
                best_val = val
                best_move = i
        return root.children[best_move]

    # Make decision of placing a piece, call Board.placePiece() function to update the board.
    def makePlace(self):
        pass
    #   return place. (,).
