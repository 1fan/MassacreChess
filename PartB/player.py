from board import Board
from piece import Piece
from referee import _InvalidActionException


class player:
    # initialize: turns, board, phase, color:'white' or 'black'
    def __init__(self, colour):
        self.color = colour
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
        pass
    #   return move. ((),())

    # Make decision of placing a piece, call Board.placePiece() function to update the board.
    def makePlace(self):
        pass
    #   return place. (,).
