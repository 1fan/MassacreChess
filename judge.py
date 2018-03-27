def isEnemy(node, coordinate, direction):
    neighbor = neighborOf(coordinate, direction)
    if isCorner(neighbor):
        return True
    if isBlack(node, neighbor):
        return isWhite(node, coordinate)
    if isWhite(node, neighbor):
        return isBlack(node, coordinate)
    return False


def isKilled(node, coordinate):
    left, right, up, down = (-1, 0), (+1, 0), (0, -1), (0, +1)
    return (isEnemy(node, coordinate, left) and isEnemy(node, coordinate, right)) \
        or (isEnemy(node, coordinate, up) and isEnemy(node, coordinate, down))


def printMoves(node):
    m = 0
    for p in node.white:
        m += count4dMove(node, p)
    print(m)
    m = 0
    for p in node.white:
        m += count4dMove(node, p)
    print(m)


def isCorner(coordinate):
    corners = [(0, 0), (0, 7), (7, 0), (7, 7)]
    return coordinate in corners


def isOutside(coordinate):
    c, r = coordinate
    return c <= -1 or c >= 8 or r <= -1 or r >= 8


def isBlack(node, coordinate):
    return coordinate in node.black


def isWhite(node, coordinate):
    return coordinate in node.white


# "-" in board
def isEmpty(node, coordinate):
    return not (isOutside(coordinate) or isCorner(coordinate) or isBlack(node, coordinate) or isWhite(node, coordinate))


def isOccupied(node, coordinate):
    return isBlack(node, coordinate) or isWhite(node, coordinate)


def neighborOf(coordinate, direction):
    directions = [(0, -1), (0, +1), (-1, 0), (1, 0)]
    return tuple(map(sum, zip(coordinate, directions[direction])))

def canMove(node, coordinate, direction):
    return isEmpty(node, neighborOf(coordinate, direction))


def canJump(node, coordinate, direction):
    neighbor = neighborOf(coordinate, direction)
    neighbor1 = neighborOf(neighbor, direction)
    return isOccupied(node, neighbor) and isEmpty(node, neighbor1)


# Check if one piece can move in one specific direction
def count1dMove(node, coordinate, direction):
    return canMove(node, coordinate, direction) + canJump(node, coordinate, direction)


# Count number of moves that one piece can make
def count4dMove(node, coordinate):
    m = 0
    for d in range(4):
        m += count1dMove(node, coordinate, d)
    return m

# find the nearest white piece to the black piece whose location is coordinate.
def findNearstWhite(node, coordinate):
    # return the position of the white piece.
    pass

def getManhattanDistance(P1, P2):
    # return the Manhattan distance of these two position.
    pass

# return possible directions from W to B.
def getPossibleDirection(B,W):
    pass
