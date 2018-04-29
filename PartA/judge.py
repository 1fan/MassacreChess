# Status of a given position
def is_corner(coordinate):
    corners = [(0, 0), (0, 7), (7, 0), (7, 7)]
    return coordinate in corners


def is_outside(coordinate):
    c, r = coordinate
    return c <= -1 or c >= 8 or r <= -1 or r >= 8


def is_black(node, coordinate):
    return coordinate in node.black


def is_white(node, coordinate):
    return coordinate in node.white


def is_enemy(node, coordinate, direction):
    neighbor = neighbor_of(coordinate, direction)
    if is_corner(neighbor):
        return True
    if is_black(node, neighbor):
        return is_white(node, coordinate)
    if is_white(node, neighbor):
        return is_black(node, coordinate)
    return False


# return whether the coordinate could be killed
def is_killed(node, coordinate):
    left, right, up, down = (-1, 0), (+1, 0), (0, -1), (0, +1)
    return (is_enemy(node, coordinate, left) and is_enemy(node, coordinate, right)) \
        or (is_enemy(node, coordinate, up) and is_enemy(node, coordinate, down))


# print the moves of white side and black side separately
def print_moves(node):
    m = 0
    for p in node.white:
        m += count_4d_move(node, p)
    print(m)
    m = 0
    for p in node.white:
        m += count_4d_move(node, p)
    print(m)





# "-" in board
def is_empty(node, coordinate):
    return not (is_outside(coordinate) or is_corner(coordinate)
                or is_black(node, coordinate) or is_white(node, coordinate))


# return whether the coordinate is occupied by a piece
def is_occupied(node, coordinate):
    return is_black(node, coordinate) or is_white(node, coordinate)


# return the coordinate of the neighbor in th specific direction
def neighbor_of(coordinate, direction):
    return add_tuples(coordinate, direction)


# return whether the coordinate could move in one direction
def can_move(node, coordinate, direction):
    return is_empty(node, neighbor_of(coordinate, direction))


# return the coordinate after the MOVE
def move(coordinate, direction):
    return add_tuples(coordinate, direction)


# return whether the coordinate could jump in the specific direction
def can_jump(node, coordinate, direction):
    neighbor = neighbor_of(coordinate, direction)
    neighbor1 = neighbor_of(neighbor, direction)
    return is_occupied(node, neighbor) and is_empty(node, neighbor1)


# return the coordinate after the JUMP
def jump(coordinate, direction):
    return add_tuples(coordinate, multiply_tuples(direction, 2))


def add_tuples(t1, t2):
    x1, y1 = t1
    x2, y2 = t2
    return x1 + x2, y1 + y2


def multiply_tuples(t, factor):
    x, y = t
    return x * factor, y * factor


# Check if one piece can move in one specific direction
def count_1d_move(node, coordinate, direction):
    return can_move(node, coordinate, direction) + can_jump(node, coordinate, direction)


# Count number of moves that one piece can make
def count_4d_move(node, coordinate):
    m = 0
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for d in range(4):
        m += count_1d_move(node, coordinate, directions[d])
    return m


# return the Manhattan distance of these two position.
def get_manhattan_distance(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x2 - x1) + abs(y2 - y1)


# return possible directions from W to B's neighbor.
def get_coordinates_after_possible_moves(node, start):
    coordinates_after_possible_moves = []
    for d in [(0, -1), (0, +1), (-1, 0), (1, 0)]:
        if can_move(node, start, d):
            coordinates_after_possible_moves.append(move(start, d))
        elif can_jump(node, start, d):
            coordinates_after_possible_moves.append(jump(start, d))
    return coordinates_after_possible_moves


def print_massacre(route):
    for oneMove in route:
        print("%s -> %s" % (oneMove[0], oneMove[1]))
