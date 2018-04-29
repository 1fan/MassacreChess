# HELPERS
WHITE, BLACK, CORNER, BLANK, OUTSIDE = ['O','@','X','-',' ']
ENEMIES = {WHITE: {BLACK, CORNER}, BLACK: {WHITE, CORNER}}
FRIENDS = {WHITE: {WHITE, CORNER}, BLACK: {BLACK, CORNER}}

DIRECTIONS = UP, DOWN, LEFT, RIGHT = (0, -1), (0, 1), (-1, 0), (1, 0)
B, W = [0, 1]




# CLASSES

class Board:
    def __init__(self, range, turn, grid, white_pieces, black_pieces):
        """
        grid for checking blank or cornor or black or white or outside
        list for calculating properties for each player
        """
        self.range = (0, 7)
        self.turn = turn
        self.grid = {} #!!!!!!!!!!!!!!!!  initialise this !!!!!!!!!!!!!!!!!!!!!!
        self.pieces = [black_pieces, white_pieces]
    """
    update board
        1.make move(place/move/jump and kill)
        2.shrink board
            range = step(range, (+1, -1))
            corner = 'X'
    """


class player:
    def __init__():
        self.colour = colour # B or W (0 or 1)
        self.pieces = []
        self.n_pieces_on_board = 0 #sizeof(pieces)
        self.n_pieces_killed_in_one_move = 0
        self.n_total_possible_moves
        self.n_moves_to_be_all_killed
        self.n_pieces_on_edges


    def get_n_pieces_on_board():
        return len(self.pieces)


    def get_n_pieces_killed_in_one_move():
        n = 0
        for piece in self.pieces:
            if piece.n_killed_moves == 1:
                n ++
        return n


    def get_n_total_possible_moves():
        n = 0
        for piece in self.pieces:
            n += piece.n_possible_moves
        return n


    def get_n_moves_to_be_all_killed():
        n = 0
        for piece in self.pieces:
            n += piece.n_killed_moves
        return n

    def get_n_pieces_on_edges():
        n = 0
        for piece in self.pices:
            c, r = piece.pos
            if c in piece.board.range or r in piece.board.range:
                n++
        return n




    #how many moves it takes so that this piece is killed
    def get_killed _moves(self):
        #def __init__(self, victim, killer, route, cost)
        me = self.player.colour
        opponent = !self.player.colour

        current_node = (self.board.pieces[me], self.board.pieces[opponent], [], 0)
        PQ = []
        PQ.append(current_node)
        target = self.pos

        for opponent_piece in current_node.killer:
            possible_moves = possible_moves(opponent_piece)
            if possible_moves:
                for new_opponent_piece in possible_moves:
                    # move

                    '''
                    # move
                    create_new_node

                    #kill
                    if kills neighbor:
                        if killed neighbor is this piece(my):
                            return len(new_route)
                        else:
                            new_node.victim.remove(neighbor)
                    # killed
                    if killed:
                        new_node.killer.remove(new_opponent_piece)
                    PQ.append

                    '''






class Node(object):
    cost = 0
    heuristic = 0
    f = cost + heuristic
    route = []
    victim = []
    killer = []

    def __init__(self, victim, killer, route, cost):
        self.route = route
        self.killer = killer
        self.victim = victim
        self.cost = cost
        self.heuristic = self.get_h()
        self.f = self.heuristic + self.cost

    def __repr__(self):
        return repr((self.victim, self.killer, self.route, self.heuristic))

    # The heuristic method to calculate the heuristic value which equals
    # the total manhattan distance between all killer pieces to the target victim piece.
    def get_h(self):
        h = 0
        b = self.victim[0]  # the victim piece to be eliminated
        for W in self.killer:
            h += get_manhattan_distance(b, W)
        return h
