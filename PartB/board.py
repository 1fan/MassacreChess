from referee import _InvalidActionException
from piece import Piece
from judge import *

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
        self.weights = (1, 2, 3, 4, 5) # Should be set to reasonable values
        self.turns = 0

    # Return a tuple of all features
    def get_features(self, color, turns):
        n_alive, n_danger, n_edge, n_safe, n_moves = 0, 0, 0, 0, 0
        directions = [[(0, -1), (0, 1)], [(-1, 0), (1, 0)]]
        enemy = 1 - color
        for piece in self.Pieces[color]:
            # Feature1: Left piece number of one color
            n_alive += 1
            # Feature5: number of pieces that could not be killed.
            if is_safe(self, color, piece.location):
                n_safe += 1
            # Feature2: The number of pieces that could be killed in 1 move. Return the number.
            else:
                for d in directions:
                    neighbor_location = add(piece.location, d)
                    neighbor_status = get_status(self, neighbor_location)
                    # Neighbor is empty
                    if neighbor_status == enemy or neighbor_status == CORNER:
                        other_neighbor_location = add(piece.location, mul(d, -1))
                        other_neighbor_status = get_status(self, other_neighbor_location)
                        # have empty spot
                        if other_neighbor_status == EMPTY and can_move_to(self, enemy, other_neighbor_location, d):
                            n_danger += 1
                    # Feature3: The number of pieces that locate at edges.
                    x, y = piece.location
                    edges = self.Corner[1]
                    if x in edges or y in edges:
                        n_edge += 1
        # Feature3:
        f_edge = get_f_edge(n_edge, turns)
        # Feature4: number of total possible moves. return the number
        f_moves = len(self.possible_moves(color))
        return n_alive, n_danger, f_edge, f_moves, n_safe

    # Make a move. move: ((x0,y0),(x1,y1))
    def move_piece(self, action, color):
        if self.judgeValidMove(action):
            # 1: update the moved piece in the list.
            self.do(action, color)
            self.start_fight(action[1], color)
            # Record features
        else:
            raise _InvalidActionException

    # Move a piece (change its location)
    def do(self, action, color):
        for piece in self.Pieces[color]:
            if piece.location == action[0]:
                piece.location = action[1]

    # Insert the piece into the list accordingly
    def place_piece(self, action, color):
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

    # Eliminate a piece
    def eliminate(self, location, color):
        for piece in self.Pieces[color]:
            if piece.location == location:
                self.Pieces[color].remove(piece)

    # Eliminate pieces located at the edge, Update the Black and White list.
    def eliminate_edge_piece(self):
        for color in [BLACK, WHITE]:
            for piece in self.Pieces[color]:
                x, y = piece.location
                edges = self.Corner[1]
                if x in edges or y in edges:
                    self.eliminate((x, y), color)

    # turns=128, 192
    def shrink_board(self, turns):
        self.Range = add(self.Range, (1, -1))
        if turns == 128:
            self.Corner = [(1, 1), (1, 6), (6, 1), (6, 6)]
        elif turns == 196:
            self.Corner = [(2, 2), (2, 5), (5, 2), (5, 5)]
        self.eliminate_edge_piece()
        return

    # Judge whether it is valid to place a piece. piece is an instance of Piece class.
    def judgeValidPlace(self, piece):
        pass

    # Judge whether it is valid to move a piece. move: ((x0,y0),(x1,y1))
    def judgeValidMove(self, move):
        pass


    # Return a list of all possible placement action ()
    # the place should be in its zone
    def possible_places(self, color):
        pass

    # Return a list of all possible move action ((),())
    def possible_moves(self, color):
        possible_moves = []
        directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]
        enemy = 1 - color
        for piece in self.Pieces[color]:
            for d in directions:
                neighbor_location = add(piece.location,d)
                neighbor_status = get_status(self, neighbor_location)
                # Can move?
                if neighbor_status == EMPTY:
                    possible_moves.append((piece.location, neighbor_location))
                # What about jump?
                elif neighbor_status == enemy:
                    opposite_location = add(neighbor_location,d)
                    opposite_status = get_status(self, opposite_location)
                    if opposite_status == EMPTY:
                        possible_moves.append((piece.location, opposite_location))
            return possible_moves

    def game_ended(self):
        if len(self.Pieces[BLACK]) == 0:
            return True
        if len(self.Pieces[WHITE]) == 0:
            return True
        return False

'''
    def Alive_Piece_Number(self, color):
        return self.Pieces[color].__len__()

    # Feature2: The number of pieces that could be killed in 1 move. Return the number.
    def Dangerous_Piece_Number(self, color):
        n = 0
        directions = [[(0, -1), (0, 1)], [(-1, 0), (1, 0)]]
        enemy = 1 - color
        for piece in self.Pieces[color]:
            for d in directions:
                neighbor_location = add(piece.location, d)
                neighbor_status = get_status(self, neighbor_location)
                # Neighbor is empty
                if neighbor_status == enemy or neighbor_status == CORNER:
                    other_neighbor_location = add(piece.location, mul(d, -1))
                    other_neighbor_status = get_status(self, other_neighbor_location)
                    # have empty spot
                    if other_neighbor_status == EMPTY and can_move_to(self, enemy, other_neighbor_location, d):
                        n += 1
                        break
        return n

    # Feature3: The number of pieces that locate at edges.
    # if turns<128 : return numbers*turns/128, if 128<turns<196 , return number*(turns-128)/(196-128)
    # if turns>196, return the number.
    def Eedge_Piece_Number(self, color, turns):
        n = 0
        for piece in self.Pieces[color]:
            x, y = piece.location
            edges = self.Corner[1]
            if x in edges or y in edges:
                n += 1
        if turns < 128:
            return n * turns / 128.0
        if turns > 196:
            return n
        else:
            return n * (turns - 128) / (196 - 128)

    # Feature4: number of total possible moves. return the number
    def Total_Possible_Moves(self, color):
        return len(self.possibleMoves(color))

    # Feature5: number of pieces that could not be killed.
    def Safe_Piece_Number(self, color):
        n = 0
        for piece in self.Pieces[color]:
            if is_safe(self,color,piece.location):
                n += 1
        return n
'''
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