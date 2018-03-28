def isEnemy(node, coordinate, direction):
    neighbor = neighborOf(coordinate, direction)
    if isCorner(neighbor):
        return True
    if isBlack(node, neighbor):
        return isWhite(node, coordinate)
    if isWhite(node, neighbor):
        return isBlack(node, coordinate)
    return False


def isKilled(node):
    coordinate = node.black[0]
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
    # directions = [(0, -1), (0, +1), (-1, 0), (1, 0)]
    return tuple(map(sum, zip(coordinate, direction)))


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
    x1, y1 = P1
    x2, y2 = P2
    return abs(x2 - x1) + abs(y2 - y1)


# return possible directions from W to B.
def getPossibleMoves(node, start, end):
    x1, y1 = start
    x2, y2 = end
    x, y = 0, 0
    if x1 > x2:  # from is on the right of to
        x = -1  # need to move left
    elif x1 < x2:  # from is on the left of to
        x = +1  # need to move right
    if y1 > y2:  # from is below to
        x = +1  # need to move up
    elif x1 < x2:  # from is above to
        x = -1  # need to move down
    possibleMoves = []
    if x:
        if canMove(node, start, (x, 0)):
            possibleMoves.append((x, 0))
    if y and canMove(node, start, (0, y)):
        possibleMoves.append((0, y))
    return possibleMoves
