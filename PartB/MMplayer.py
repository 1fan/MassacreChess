from numpy import random
from board import Board
from judge import *
import operator
from node import Node
import copy

from referee import _InvalidActionException

COLLECT_MOVING = 1
COLLECT_PLACING = 0

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
            if COLLECT_PLACING:
                self.writeFile()
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
            if COLLECT_MOVING:
                self.writeFile()

            # shrink the board after my move
            if self.phase_turns in [128, 192]:
                self.board.shrink_board(self.phase_turns)

            return Best_Move

    def update(self, action):
        # adjust opponent's piece
        # if action is a nested tuple --> it is a 'move'; else --> it is a 'place'
        if action:
            enemy_color = 1 - self.color
            self.update_turns()
            # moving phase
            if isinstance(action[0], tuple):
                self.board.move_piece(action, enemy_color)
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


        # Evaluation
    def calculate_e(self):
        my_e = 0
        enemy_e = 0
        for wf in mul2list(self.board.weights, self.board.get_features(self.color, self.phase_turns)):
            my_e += wf
        for wf in mul2list(self.board.weights, self.board.get_features(1 - self.color, self.phase_turns)):
            enemy_e += wf
        return my_e - enemy_e

    def writeFile(self):
        self.FeatureValueResult = add2list(self.FeatureValueResult, self.board.get_features(self.color, self.phase_turns))
        if self.board.game_ended():
            FinalFeatureResult = [x / self.phase_turns for x in self.FeatureValueResult]

            if self.board.game_ended() - 1 == self.color:

                with open('data.txt', 'a') as f:
                    f.write(str(FinalFeatureResult) + "|" + '1')
            elif self.board.game_ended() == 3:
                with open('data.txt', 'a') as f:
                    f.write(str(FinalFeatureResult) + "|" + '0')
            elif self.board.game_ended() - 1 == 1 - self.color:
                with open('data.txt', 'a') as f:
                    f.write(str(FinalFeatureResult) + "|" + '-1')
    # Make decision of move a piece
    def best_move(self):
        # MINIMAX
        depth_limit = self.get_depth()  # must be even number for this implementation
        this_board = copy.deepcopy(self.board)
        root = Node(depth_limit, self.color, this_board, None, self.color)
        best_val = -np.inf
        best_move = 0
        if root.children is None:
            return None
        for child in root.children:
            val = child.minmax(child, depth_limit - 1, self.phase_turns + 1)
            # update best value and move for min max
            if val > best_val:
                best_val = val
                best_move = child
        return best_move.action

    # Make decision of placing a piece, call Board.placePiece() function to update the board.
    def best_place(self):
        #EVALUATION
        # Possible_Places = self.POSSIBLE_PLACE[self.color]
        # max_e = -np.inf
        # best_place = 0
        # for i in range(len(Possible_Places)):
        #     # new_Pieces = self.board.Pieces
        #     new_board = copy.deepcopy(self.board)
        #     new_board.place_piece(Possible_Places[i], self.color)
        #     node = Node(0, self.color, new_board, None, self.color)
        #     # should have a different feature function
        #     this_e = node.get_e(-1)
        #     if this_e > max_e:
        #         max_e = this_e
        #         best_place = i
        # return Possible_Places[best_place]

        randomPlace = random.randint(0, self.POSSIBLE_PLACE[self.color].__len__())
        return self.POSSIBLE_PLACE[self.color][randomPlace]

    def get_depth(self):
        if self.board.Range[1] == 6:
            return 4
        return 2