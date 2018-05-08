from numpy import random
from board import Board
from judge import *
from node import Node
import copy
import operator

COLLECT_DATA = 1

from referee import _InvalidActionException


class Player:
    # initialize: phase_turns, board, phase, color:BLACK, WHITE = 0, 1
    def __init__(self, colour):
        BLACK_POSSIBLE_PLACE = []
        WHITE_POSSIBLE_PLACE = []
        self.POSSIBLE_PLACE = [BLACK_POSSIBLE_PLACE, WHITE_POSSIBLE_PLACE]
        match_color = {'black': 0, 'white': 1}
        self.color = match_color[colour]
        self.phase = "placing"
        self.phase_turns = 0
        self.board = Board()
        self.new_board = Board()
        self.initLegalPlace()
        self.FeatureValueResult = []
        self.initFeature()

    def initFeature(self):
        if COLLECT_MOVING:
            self.FeatureValueResult = [0, 0, 0, 0, 0]
        else:
            self.FeatureValueResult = [0, 0, 0]

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
            if self.phase_turns in [128, 192]:
                self.board.shrink_board(self.phase_turns)
            # Give a best move
            Best_Move = self.best_move()

            # Make the move on my board
            self.board.move_piece(Best_Move, self.color)
            self.phase_turns += 1
            if COLLECT_DATA:
                self.writeFile()

            # shrink the board after my move
            if self.phase_turns in [128, 192]:
                self.board.shrink_board(self.phase_turns)

            return Best_Move

    def writeFile(self):
        map(operator.add, self.FeatureValueResult, self.board.get_features(self.phase_turns, self.color))
        if self.board.game_ended():
            FinalFeatureResult = [x / self.phase_turns for x in self.FeatureValueResult]
            if self.board.game_ended() - 1 == self.color:
                with open('C:/Users/thinkpad/Documents/Git/AI_Project/PartB/data.txt', 'w') as f:
                    f.write(str(FinalFeatureResult) + "|" + '1')
            elif self.board.game_ended() == 3:
                with open('C:/Users/thinkpad/Documents/Git/AI_Project/PartB/data.txt', 'w') as f:
                    f.write(str(FinalFeatureResult) + "|" + '0')
            elif self.board.game_ended() - 1 == 1 - self.color:
                with open('C:/Users/thinkpad/Documents/Git/AI_Project/PartB/data.txt', 'w') as f:
                    f.write(str(FinalFeatureResult) + "|" + '-1')

    def update(self, action):
        # adjust opponent's piece
        # if action is a nested tuple --> it is a 'move'; else --> it is a 'place'
        if action:
            enemy_color = 1 - self.color
            self.update_turns()
            # moving phase
            if isinstance(action[0], tuple):
                self.board.move_piece(action, enemy_color)
                if COLLECT_DATA:
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
        # EVALUATION
        Possible_Moves = self.board.possible_moves(self.color)
        max_e = -np.inf
        best_move = 0
        for i in range(len(Possible_Moves)):
            new_board = copy.deepcopy(self.board)
            new_board.move_piece(Possible_Moves[i], self.color)
            node = Node(0, self.color, new_board, None, None)
            this_e = node.get_e(self.phase_turns)
            if this_e > max_e:
                max_e = this_e
                best_move = i
        return Possible_Moves[best_move]


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
