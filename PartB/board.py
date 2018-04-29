from referee import _InvalidActionException
from judge import *
from mywatchyourback import *

class Board:
    '''
    Initialize the Black/White list, store Piece instance in the list.
    Initialize weight for each features. Store each feature's value.
    '''
    def __init__(self):
        black = []
        white = []
        self.Pieces = [black, white]  # [black, white] list of Piece
        self.Range = (0, 8) # location should be in this range to be inside the board
        self.Corner = [(0,0),(0,7),(7,0),(7,7)]
        self.weight_f1, self.weight_f2, self.weight_f3, self.weight_f4, self.weight_f5 = 5,4,3,2,1

    # Feature1: Left piece number of one color
    def Self_Piece_Number(self, color):
        return self.Pieces[color].__len__()

    # Feature2: The number of pieces that could be killed in 1 move. Return the number.
    def Killed_In_1move_Number(self, color):
        pass

    # Feature3: The number of pieces that locate at edges.
    # if turns<128 : return numbers*turns/128, if 128<turns<196 , return number*(turns-128)/(196-128)
    # if turns>196, return the number.
    def Pieces_In_Edge_Number(self, color, turns):
        pass

    # Feature4: number of total possible moves. return the number
    def Total_Possible_Moves(self, color):
        pass

    # Feature5: number of pieces that could not be killed.
    def Unkilled_Piece_Number(self, color):
        pass

    # Evaluation
    def getE(self, color):
        pass

    # Make a move. move: ((x0,y0),(x1,y1))
    def movePiece(self, action, color):
        if self.judgeValidMove(action):
            # 1: update the moved piece in the list.
            self.move(action, color)
            self.start_fight(action[1], color)
            # Record features
        else:
            raise _InvalidActionException

    # Insert the piece into the list accordingly
    def placePiece(self, action, color):
        if self.judgeValidPlace(action):
            piece = Piece(action, color)
            self.Pieces[color].append(piece)
            self.start_fight(action, color)
            # Record features
        else:
            raise _InvalidActionException

    def start_fight(self, my_location, my_color):
        # check if kills others
        directions = [[(0, -1), (0, 1)], [(-1, 0), (1, 0)]]
        friend = my_color
        enemy = 1 - my_color
        me_dead = False
        for dd in directions:
            if me_dead:
                break
            for d in dd:
                neighbor_location = add(my_location, d)
                neighbor_status = get_status(self, neighbor_location)
                # Neighbor is enemy
                if neighbor_status == enemy:
                    opposite_location = add(neighbor_location, d)
                    opposite_status = get_status(self, opposite_location)
                    # neighbor enemy is killed and check next dimension
                    if opposite_status == friend or opposite_status == CORNER:
                        self.eliminate(neighbor_location, enemy)
                        break
                    # check the other neighbor enemy
                    else:
                        other_neighbor_location = add(my_location, mul(d, -1))
                        other_neighbor_status = get_status(self, other_neighbor_location)
                        # I am killed and stop the loop
                        if other_neighbor_status == enemy or other_neighbor_status == CORNER:
                            self.eliminate(my_location, my_color)
                            me_dead = True
                            break

        '''
        for direction in directions:
            neighbor_location = add(my_location, direction)
            neighbor_status = get_status(self, neighbor_location)
            # neighbor is different color
            if neighbor_status == enemy:
                opposite_location = add(neighbor_location, direction)
                opposite_status = get_status(self, opposite_location)
                if opposite_status == friend or opposite_status == CORNER:
                    self.eliminate(neighbor_location, enemy)
        # check if is killed
        for direction in directions:
            neighbor_location = add(my_location, direction)
            neighbor_status = get_status(self, neighbor_location)
            # neighbor is different color
            if neighbor_status == enemy:
                other_neighbor_location = add(my_location, mul(direction, -1))
                other_neighbor_status = get_status(self, other_neighbor_location)
                if other_neighbor_status == enemy or other_neighbor_status == CORNER:
                    self.eliminate(my_location, my_color)
                    break
        '''
    # Eliminate a piece
    def eliminate(self, location, color):
        for piece in self.Pieces[color]:
            if piece.location == location:
                self.Pieces[color].remove(piece)

    # Move a piece (change its location)
    def move(self, action, color):
        for piece in self.Pieces[color]:
            if piece.location == action[0]:
                piece.location = action[1]

    # Eliminate pieces located at the edge, Update the Black and White list.
    def eliminate_EdgePiece(self,turns):
        if turns == 128:
            pass
        elif turns == 196:
            pass

    # turns=128, 192
    def shrinkBoard(self, turns):
        if turns == 128:
            self.Corner = [(1,1), (1,6), (6,1),(6,6)]
            self.Range = add(self.Range, (1, -1))
            self.eliminate_EdgePiece(turns)
        elif turns == 196:
            self.Corner = [(2, 2), (2, 5), (5, 2), (5, 5)]
            self.Range = add(self.Range, (1, -1))
            self.eliminate_EdgePiece(turns)

    # Judge whether it is valid to place a piece. piece is an instance of Piece class.
    def judgeValidPlace(self, piece):
        pass
    # Judge whether it is valid to move a piece. move: ((x0,y0),(x1,y1))
    def judgeValidMove(self, move):
        pass
    # Return a list of all possible moves
    def possibleMoves(self, color):
        pass




    def check_win(self):
        pass
