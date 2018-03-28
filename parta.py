from Node import *
from judge import *
import queue

def readFile(path):
    r = 0
    with open(path, 'r') as f:
        for line in f.readlines():
            if r == 8:
                action = line.strip()
                if action=="Moves":
                    return 1
                elif action=="Massacre":
                    return 2
                else:
                    print("Invalid Command")
                    exit(-1)

            else:
                newline = []
                c = 0
                for ch in line.strip():
                    if ch == "O":
                        white.append((c, r))
                    elif ch == "@":
                        black.append((c, r))
                    if ch != " ":
                        newline.append(ch)
                        c += 1
                board.append(newline)
                r += 1

if __name__ == "__main__":
    board = []  # 2d list of the board
    black = []  # list of all black pieces
    white = []  # list of all white pieces
    PriorityList = [] # using sorted(PriorityList, key=lambda Node: Node.G) to sort using the value G
    if(readFile("files/massacre-sample-1.in") == 1):
        node0 = Node(black, white, [],0)
        printMoves(node0)
    else:
        node0 = Node(black, white, [],0)
        Target = Node([], [], [],0)
        PriorityList.append(node0)
        totalRoute = []
        node = node0
        while not isKilled(node):
            node = sorted(PriorityList, key=lambda Node: Node.G)[0]     # pop out
            PriorityList.pop(0)
            B = node.black[0]
            for direction in [(0, -1), (0, +1), (-1, 0), (1, 0)]:
                # find next moves
                neighbor = neighborOf(B, direction)
                WhitePosition = findNearstWhite(node, neighbor)
                possibleNextMove = getPossibleMoves(node, WhitePosition, neighbor)

                # generate new node for each move
                if possibleNextMove:
                    for m in possibleNextMove:
                        addedRoute = [WhitePosition, m]  # list of tuples
                        newWhite = node.white.remove(WhitePosition)
                        newWhite.append(m)

                        newNode = Node(black, newWhite, node.route.append(addedRoute), node.cost + 1)
                        PriorityList.append(newNode)
                        if isKilled(newNode):
                            totalRoute.append(newNode.route)
                            Target = newNode
                            newNode.black.remove(B)
                            break
                        else:
                            PriorityList.append(newNode)
        PriorityList = [].append(Target)

        print(Target.route)








