from referee import _InvalidActionException

class Board:
    '''
    Initialize the Black/White list, store Piece instance in the list.
    Initialize weight for each features. Store each feature's value.
    '''
    def __init__(self):
        self.WhitePieces = []
        self.BlackPieces = []
        self.Range = 8
        self.Corner = [(0,0),(0,7),(7,0),(7,7)]
        self.weight_f1, self.weight_f2, self.weight_f3, self.weight_f4, self.weight_f5 = 5,4,3,2,1

    # Feature1: Left piece number of one color
    def Self_Piece_Number(self, color):
        if color=='white':
            return self.WhitePieces.__len__()
        else:
            return self.BlackPieces.__len__()

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

    # Make a move. move: ((x0,y0),(x1,y1))
    def movePiece(self, move):
        if self.judgeValidMove(move):
            # update the moved piece in the list.
            pass
        else:
            raise _InvalidActionException

    #Insert the piece into the list accordingly
    def placePiece(self,piece):
        if self.judgeValidPlace(piece):
            if piece.color == 'white':
                self.WhitePieces.append(piece)
            else:
                self.BlackPieces.append(piece)
        else:
            raise _InvalidActionException

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
            self.Range -= 1
            self.eliminate_EdgePiece(turns)
        elif turns == 196:
            self.Corner = [(2, 2), (2, 5), (5, 2), (5, 5)]
            self.Range -= 1
            self.eliminate_EdgePiece(turns)

    # Judge whether it is valid to place a piece. piece is an instance of Piece class.
    def judgeValidPlace(self, piece):
        pass
    # Judge whether it is valid to move a piece. move: ((x0,y0),(x1,y1))
    def judgeValidMove(self, move):
        pass