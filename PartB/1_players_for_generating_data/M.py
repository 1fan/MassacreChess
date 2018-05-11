from numpy import random
from board import Board
from helpers import *
from node import Node
import copy

# These two value is used in checking collect data for moving or placing.
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
        self.my_FeatureValueResult = []
        self.op_FeatureValueResult = []
        self.initFeature()

    # Init value for features.
    def initFeature(self):
        if COLLECT_MOVING:
            self.my_FeatureValueResult = [0, 0, 0, 0, 0]
            self.op_FeatureValueResult = [0, 0, 0, 0, 0]
        else:
            self.my_FeatureValueResult = [0, 0, 0]

    # Init all legal possible places for duel sides.
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
        # if action is a nested tuple-> it is a 'move'; else-->it is a 'place'
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

    # Update phase from placing to moving.
    def update_turns(self):
        self.phase_turns += 1
        if self.phase == "placing" and self.phase_turns == 24:
            self.phase = "moving"
            self.phase_turns = 0

    # Remove a specific place from possible placing list.
    def remove_from_possible_place(self, location):
        c ,r = location
        if r in range(2, 8):
            self.POSSIBLE_PLACE[BLACK].remove(location)
        if r in range(0, 6):
            self.POSSIBLE_PLACE[WHITE].remove(location)

    # Calculate the evaluation value
    def calculate_e(self):
        my_e = 0
        enemy_e = 0
        for wf in mul2list(self.board.weights, 
            self.board.get_features(self.color, self.phase_turns)):
            my_e += wf
        for wf in mul2list(self.board.weights, 
            self.board.get_features(1 - self.color, self.phase_turns)):
            enemy_e += wf
        return my_e - enemy_e

    # Write the feature value and fight result in a file for ML.
    def writeFile(self):
        self.my_FeatureValueResult = add2list(self.my_FeatureValueResult, 
            self.board.get_features(self.color, self.phase_turns))
        self.op_FeatureValueResult = add2list(self.op_FeatureValueResult,
            self.board.get_features(1-self.color, self.phase_turns-1))
        if self.phase_turns > 200:
            winner = self.dead_loop()
        else:
            winner = self.board.game_ended()
        if winner:
            my_FinalFeatureResult = 
            [x / self.phase_turns for x in self.my_FeatureValueResult]
            op_FinalFeatureResult = 
            [x / self.phase_turns for x in self.op_FeatureValueResult]

            if winner - 1 == self.color:
                with open('data.txt', 'a') as f:
                    f.write(str(my_FinalFeatureResult) + '1\n')
                    f.write(str(op_FinalFeatureResult) + '-1\n')
            elif winner == 3:
                with open('data.txt', 'a') as f:
                    f.write(str(my_FinalFeatureResult) + '0\n')
                    f.write(str(op_FinalFeatureResult) + '0\n')
            elif winner - 1 == 1 - self.color:
                with open('data.txt', 'a') as f:
                    f.write(str(my_FinalFeatureResult) + '-1\n')
                    f.write(str(op_FinalFeatureResult) + '1\n')

    # If dead loop occurs, judge which side win.
    def dead_loop(self):
        n_black = len(self.board.Pieces[BLACK])
        n_white = len(self.board.Pieces[WHITE])
        if n_black > n_white:
            return BLACK +1
        elif n_black < n_white:
            return WHITE + 1
        else:
            return 3

    # Make decision of moving a piece
    def best_move(self):
        # MINIMAX
        depth_limit = self.get_depth()  
        this_board = copy.deepcopy(self.board)
        root = Node(depth_limit, self.color, this_board, None, self.color)
        best_val = -np.inf
        best_move = 0
        if root.children is None:
            return None
        for child in root.children:
            val = child.minmax(depth_limit - 1, self.phase_turns + 1)
            # update best value and move for min max
            if val > best_val:
                best_val = val
                best_move = child
        return best_move.action

    # Make decision of placing a piece, 
    # call Board.placePiece() function to update the board.
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

        randomPlace = random.randint(0, 
            self.POSSIBLE_PLACE[self.color].__len__())
        return self.POSSIBLE_PLACE[self.color][randomPlace]

    def get_depth(self):
        if self.board.Range[1] == 6:
            return 4
        return 2