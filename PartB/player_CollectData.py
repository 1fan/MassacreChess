from numpy import random
from board import Board
from judge import *
from node import Node
import copy
import operator

from referee import _InvalidActionException


class Player:
    # initialize: phase_turns, board, phase, color:BLACK, WHITE = 0, 1
    def __init__(self, colour):
        BLACK_POSSIBLE_PLACE = []
        WHITE_POSSIBLE_PLACE = []
        self.FeatureValueResult = []
        self.POSSIBLE_PLACE = [BLACK_POSSIBLE_PLACE,WHITE_POSSIBLE_PLACE]
        match_color = {'black': 0, 'white': 1}
        self.color = match_color[colour]
        self.phase = "placing"
        self.phase_turns = 0
        self.board = Board()
        self.new_board = Board()
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
            Best_Place = self.best_place()
            self.remove_from_possible_place(Best_Place)
            self.board.place_piece(Best_Place, self.color)
            self.update_turns()
            return Best_Place

        if self.phase == "moving":
            # shrink the board before my move
            if turns in [128, 196]:
                self.board.shrink_board(turns)
            # Give a best move
            Best_Move = self.best_move()

            # Make the move on my board
            self.board.move_piece(Best_Move, self.color)
            self.writeFile()
            map(operator.add,self.FeatureValueResult, self.board.get_features(self.phase_turns, self.color))
            self.phase_turns += 1

            # shrink the board after my move
            turns += 1
            if turns in [128, 196]:
                self.board.shrink_board(turns)

            return Best_Move

    def writeFile(self):
        if self.board.game_ended() - 1 == self.color:
            with open('data', 'w') as f:
                f.write(str(self.FeatureValueResult) + "|" + '1')
        elif self.board.game_ended() == 3:
            with open('data', 'w') as f:
                f.write(str(self.FeatureValueResult) + "|" + '0')
        elif self.board.game_ended() - 1 == 1 - self.color:
            with open('data', 'w') as f:
                f.write(str(self.FeatureValueResult) + "|" + '-1')

    def update(self, action):
        # adjust opponent's piece
        # if action is a nested tuple --> it is a 'move'; else --> it is a 'place'
        if action:
            enemy_color = 1 - self.color
            self.update_turns()
            # moving phase
            if isinstance(action[0], tuple):
                self.board.move_piece(action, enemy_color)
                self.writeFile()
            # placing phase
            else:
                self.board.place_piece(action, enemy_color)
                self.remove_from_possible_place(action)

    def update_turns(self):
        self.phase_turns += 1
        if self.phase == "placing" and self.phase_turns == 24:
            self.phase = "moving"
            self.phase_turns = 0


    def remove_from_possible_place(self, location):
        c ,r = location
        if r in range(2, 8):
            self.POSSIBLE_PLACE[BLACK].remove(location)
        if r in range(0, 6):
            self.POSSIBLE_PLACE[WHITE].remove(location)

    # Make decision of move a piece
    def best_move(self):
        # MINIMAX
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

        # EVALUATION
        Possible_Moves = self.board.possible_moves(self.color)
        max_e = -np.inf
        best_move = 0
        for i in range(len(Possible_Moves)):
            # new_Pieces = self.board.Pieces
            self.new_board = copy.deepcopy(self.board)
            # self.board.print_board()
            self.new_board.move_piece(Possible_Moves[i], self.color)
            # self.board.print_board()
            node = Node(0, self.color, self.new_board, None)
            this_e = node.get_e(self.phase_turns)
            if this_e > max_e:
                max_e = this_e
                best_move = i
        return Possible_Moves[best_move]

        # RAMDOM
        # Possible_Moves = self.board.possible_moves(self.color)
        # if Possible_Moves is None:
        #     return None
        # else:
        #     randomMove = random.randint(0, Possible_Moves.__len__())
        #     return Possible_Moves[randomMove]





    # Make decision of placing a piece, call Board.placePiece() function to update the board.
    def best_place(self):
        randomPlace = random.randint(0,self.POSSIBLE_PLACE[self.color].__len__())
        return self.POSSIBLE_PLACE[self.color][randomPlace]
    #   return place. (,).

        # Evaluation
    def calculate_e(self):
        my_e = 0
        enemy_e = 0
        for wf in mul2list(self.board.weights, self.board.get_features(self.color, self.phase_turns)):
            my_e += wf
        for wf in mul2list(self.board.weights, self.board.get_features(1 - self.color, self.phase_turns)):
            enemy_e += wf
        return my_e - enemy_e
