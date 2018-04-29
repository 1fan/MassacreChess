# Helper
EMPTY, BLACK, WHITE, CORNER, OUTSIDE = -1, 0, 1, 2, 3

ZONE = [get_zone(2, 7), get_zone(0, 5)]

def get_zone(x, y):
    zone = []
    for c in range(8):
        for r in range(x, y+1):
            zone.append((c, r))
    return zone

def add(tup1, tup2):
    x1, y1 = tup1
    x2, y2 = tup2
    return x1+x2, y1+y2


def mul(tup, factor):
    x, y = tup
    return factor * x, factor * y


# Status of a given position
def get_status(board, location):
    x, y = location
    minr, maxr = board.Range
    if not (x in range(minr, maxr) and y in range(minr, maxr)):
        return OUTSIDE
    if location in board.Corner:
        return CORNER
    for piece in board.Pieces[BLACK]:
        if piece.location == location:
            return BLACK
    for piece in board.Pieces[WHITE]:
        if piece.location == location:
            return WHITE
    return EMPTY


# check if given player can move a piece to this location from directions other than the given one
def can_move_to(board, color, location, d):
    directions = [[(0, -1), (0, 1)], [(-1, 0), (1, 0)]]
    directions.remove(d)
    for direction in directions:
        neighbor_location = add(location.location, direction)
        neighbor_status = get_status(board, neighbor_location)
        if neighbor_status == color:
            return True
        if neighbor_status == 1 - color:
            opposite_location = add(neighbor_location, direction)
            opposite_status = get_status(board, opposite_location)
            if opposite_status == color:
                return True
    return False


def is_safe(board, color, location):
    UP, DOWN, LEFT, RIGHT = (0, -1), (0, 1), (-1, 0), (1, 0)
    u = get_status(board, add(location, UP))
    d = get_status(board, add(location, DOWN))
    l = get_status(board, add(location, LEFT))
    r = get_status(board, add(location, RIGHT))
    safe = [color, OUTSIDE]
    return (u in safe or d in safe) and (l in safe or r in safe)




