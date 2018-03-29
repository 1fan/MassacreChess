from NodeFINAL import *
from judgeFINAL import *

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
    if(readFile("files/massacre-sample-3.in") == 1):
        node0 = Node(black, white, [],0)
        printMoves(node0)
    else:
        #black.reverse()
        node0 = Node(black, white, [], 0)    # initial state
        # totalRoute = []                      keep track off the overall route
        PriorityList.append(node0)
        node = node0
        # try to kill each of the black pieces in turn
        # for B in node0.black:

        isAllKilled = False
        while not isAllKilled:  # target black is not killed
            isNotKilled = True  # B
            #node = PriorityList.pop(0)
            B = node.black[0]
            for W0 in node.white:
                W_list = getPossibleMoves(node, W0)
                if W_list:
                    for W in W_list:
                        newRoute = list(node.route)
                        newRoute.append([W0, W])
                        newWhite = list(node.white)
                        newWhite.remove(W0)
                        newWhite.append(W)
                        newNode = Node(node.black, newWhite, newRoute, node.cost + 1)

                        killByAccident = False
                        for Black in newNode.black:
                            if Black != B and isKilled(newNode, Black):
                                # print("Accidently killed %s" % (Black,))
                                killByAccident = True
                                break
                        if killByAccident:
                            break


                        if isKilled(newNode, B):
                            # print("Targeted %s killed" % (B,))
                            isNotKilled = False
                            printMassacre(newNode.route)

                            # Update newNode
                            newNode.black.remove(B)
                            newNode.route.clear()

                            # Update PriorityList
                            del PriorityList[:]
                            PriorityList.append(newNode)
                            break
                        else:
                            PriorityList.append(newNode)
                            PriorityList = sorted(PriorityList, key=lambda Node: Node.G)
                    if not isNotKilled:
                        break
            # Check is all killed
            node = PriorityList.pop(0)
            if not node.black:
                isAllKilled = True

