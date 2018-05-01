from numpy import random
from board import Board
from judge import *
from node import Node
from referee import _InvalidActionException


class Player:
    # initialize: phase_turns, board, phase, color:BLACK, WHITE = 0, 1
    def __init__(self, colour):
        BLACK_POSSIBLE_PLACE = []
        WHITE_POSSIBLE_PLACE = []
        self.POSSIBLE_PLACE = [BLACK_POSSIBLE_PLACE,WHITE_POSSIBLE_PLACE]
        match_color = {'black': 0, 'white': 1}
        self.color = match_color[colour]
        self.phase = "placing"
        self.phase_turns = 0
        self.board = Board()
        self.initLegalPlace()

    def initLegalPlace(self):
        for c in range(0,8):
            for r in range(2,8):
                self.POSSIBLE_PLACE[BLACK].append((c, r))
        self.POSSIBLE_PLACE[BLACK].remove((0, 7))
        self.POSSIBLE_PLACE[BLACK].remove((7, 7))
        for c in range(0,8):
            for r in range(0,6):
                self.POSSIBLE_PLACE[WHITE].append((c,r))
        self.POSSIBLE_PLACE[WHITE].remove((0, 0))
        self.POSSIBLE_PLACE[WHITE].remove((7, 0))

    def action(self, turns):
        if self.phase == "placing":
            if turns < 24:
                self.phase_turns += 1
                Best_Place = self.best_place()
                self.POSSIBLE_PLACE[self.color].remove(Best_Place)
                return Best_Place
            elif turns == 24:
                self.phase = "moving"
                self.phase_turns = 0

        if self.phase == "moving":
            # shrink the board before my move
            if turns in [128, 196]:
                self.board.shrink_board(turns)

            # Give a best move
            Best_Move = self.best_move()

            # Make the move on my board
            self.board.place_piece(Best_Move, self.color)
            self.phase_turns += 1

            # shrink the board after my move
            turns += 1
            if turns in [128, 196]:
                self.board.shrink_board(turns)

            return Best_Move

    def update(self, action):
        # adjust opponent's piece
        # if action is a nested tuple --> it is a 'move'; else --> it is a 'place'
        enemy_color = 1 - self.color
        if isinstance(action[0], tuple):
            self.board.move_piece(action, enemy_color)
        elif isinstance(action[0], int):
            self.board.place_piece(action, enemy_color)
            self.POSSIBLE_PLACE[1-self.color].remove(action)
        else:
            raise _InvalidActionException

    # Make decision of move a piece
    def best_move(self):
        # depth_limit = 4  # must be even number for this implementation
        # root = Node(depth_limit, self.color, self.board, None)
        # # d%2 == 0 -> min's move -> +inf
        # # d%2 == 1 -> max's move -> -inf
        #
        # best_val = root.children[0].value
        # best_move = 0
        # i = 0
        # for child in root.children:
        #     val = child.minmax(child, depth_limit - 1, self.phase_turns)
        #     # update best value and move for min max
        #     if ((child.depth % 2 == 0) and (val < best_val)) or ((child.depth % 2 == 1) and (val > best_val)):
        #         best_val = val
        #         best_move = i
        # return root.children[best_move]
        Possible_Moves = self.board.possible_moves(self.color)
        randomMove = random.randint(0, Possible_Moves.__len__())
        return Possible_Moves[randomMove]
        pass


    # Make decision of placing a piece, call Board.placePiece() function to update the board.
    def best_place(self):
        randomPlace = random.randint(0,self.POSSIBLE_PLACE[self.color].__len__())
        return self.POSSIBLE_PLACE[self.color][randomPlace]
    #   return place. (,).
