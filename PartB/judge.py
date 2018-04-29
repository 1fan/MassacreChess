# Helper
EMPTY, BLACK, WHITE, CORNER, OUTSIDE = -1, 0, 1, 2, 3


def add(tup1, tup2):
    x1,y1 = tup1
    x2,y2 = tup2
    return x1+x2, y1+y2


def mul(tup, factor):
    x, y = tup
    return factor * x, factor * y


# Status of a given position
def get_status(board, location):
    x, y = location
    minr, maxr = board.Range
    if location in board.Corner:
        return CORNER
    if not x in range(minr, maxr) and y in range(minr, maxr):
        return OUTSIDE
    for piece in board.Pieces[BLACK]:
        if piece.location == location:
            return BLACK
    for piece in board.Pieces[WHITE]:
        if piece.location == location:
            return WHITE
    return EMPTY


