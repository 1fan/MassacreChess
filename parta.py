from Node import *
from judge import *
import queue


def printMassacre(route):
    for oneMove in route:
        print("%s -> %s" % (oneMove[0], oneMove[1]))


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
    PriorityList = [] # re-sort the list each time after adding a new node
    if(readFile("files/massacre-sample-2.in") == 1):
        node0 = Node(black, white, [],0)
        printMoves(node0)
    else:
        black.reverse()
        node0 = Node(black, white, [],0)    # initial state
        Target = Node([], [], [],0)         # the state when one black piece has been killed
        totalRoute = []                     # keep track off the overall route
        PriorityList.append(node0)
        node = node0
        # try to kill each of the black pieces in turn
        # for B in node0.black:

        isNotKilled = True  # B
        while isNotKilled:  # target black is not killed
            B = node.black[0]
            node = PriorityList.pop(0)
            #print(node.G)
            for direction in [(0, -1), (0, +1), (-1, 0), (1, 0)]:
                # find next moves
                neighbor = neighborOf(B, direction)
                WhitePosition = findNearstWhite(node, neighbor)
                possibleNextMove = getPossibleMoves(node, WhitePosition, neighbor)

                # generate new node for each move
                if possibleNextMove:
                    for m in possibleNextMove:
                        # node.route.append([WhitePosition, m])
                        newRoute = list(node.route)
                        newRoute.append([WhitePosition, m])
                        newWhite = list(node.white)
                        newWhite.remove(WhitePosition)
                        newWhite.append(m)
                        newNode = Node(node.black, newWhite, newRoute, node.cost + 1)
                        # print(newNode.G)
                        # killableMove = 0 #whether this move could kill one or more black
                        for Black in newNode.black:
                            if Black != B and isKilled(newNode, Black):
                                print("Accidently killed %s" % (Black,))
                                newNode.black.remove(Black)
                        if isKilled(newNode, B):
                            print("Targeted %s killed" % (Black,))
                            newNode.black.remove(Black)
                            Target = newNode
                            PriorityList = [].append(Target)
                            totalRoute.append(Target.route)
                            isNotKilled = False
                            # printMassacre(Target.route)
                            break

                        if isNotKilled:
                            PriorityList.append(newNode)
                            PriorityList = sorted(PriorityList, key=lambda Node: Node.G)

                    if not isNotKilled:
                        break

        for r in totalRoute:
            printMassacre(r)







