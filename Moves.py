# Count total number of moves that can be made by one player
def n_move_of_one_piece(b, color):
    m = 0
    for p in color:
        #print(p)
        #print(count4dMove(b, p))
        m += count4dMove(b, p)
    return m


def isCorner(coordinate):
    corners = [(0, 0), (0, 7), (7, 0), (7, 7)]
    return coordinate in corners


def isOutside(coordinate):
    c, r = coordinate
    return c <= -1 or c >= 8 or r <= -1 or r >= 8


def isEmpty(b, coordinate):
    c, r = coordinate
    return (not isOutside(coordinate) or isCorner(coordinate) ) and b[r][c] == "-"


def isOccupied(b, coordinate):
    c, r = coordinate
    return (not isOutside(coordinate)) and (b[r][c] == "O" or b[r][c] == "@")


# Check if one piece can move in one specific direction
def count1dMove(b, coordinate, direction):
    m = 0
    directions = [(0, -1), (0, +1), (-1, 0), (1, 0)]
    neighbor = tuple(map(sum, zip(coordinate, directions[direction])))
    neighbor1 = tuple(map(sum, zip(neighbor, directions[direction])))
    if isEmpty(b, neighbor):
        m += 1
    elif isOccupied(b, neighbor) and isEmpty(b, neighbor1):
        m += 1
    return m


# Count number of moves that one piece can make
def count4dMove(b, coordinate):
    m = 0
    for d in range(4):
        m += count1dMove(b, coordinate, d)
    return m


text = """X - - - - - - X
- - - - - - - -
- - - - - O O -
- - - - @ O - -
- - - - - - - -
- - - - - O - -
- - - - @ - @ @
X - - - - - - X
Moves"""

# read input
r = 0
board = []  # 2d list of the board
black = []  # list of all black pieces
white = []  # list of all white pieces
for line in text.split("\n"):
    if r == 8:
        action = line
    else:
        newline = []
        c = 0
        for ch in line:

            if ch == "O":
                white.append((c, r))
            elif ch == "@":
                black.append((c, r))
            if ch != " ":
                newline.append(ch)
                c += 1
        board.append(newline)
        r += 1

# Move
print(n_move_of_one_piece(board, white))
print(n_move_of_one_piece(board, black))


# for debug
def checkstatus(b, c):
    x, y = c
    print("coordinate is " + b[y][x])
    print(" outside", isOutside(c))
    print(" empty", isEmpty(b, c))
    print(" occupied", isOccupied(b, c))
    print(" corner", isCorner(c))

