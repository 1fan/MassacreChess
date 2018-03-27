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
    if(readFile("files/move-sample-1.in") == 1):
        node0 = Node(black, white, [], 0)
        printMoves(node0)
    else:
        node0 = Node(black, white, [], 0)
        Target = Node([], [], [], 0)
        PriorityList.append(node0)
        totalRoute = []
        for B in black:
            while isKilled(node0, B):
                node = sorted(PriorityList, key=lambda Node: Node.G)[0]
                for direction in [(0, -1), (0, +1), (-1, 0), (1, 0)]:
                    WhitePosition = findNearstWhite(node, B)
                    huristicValue = getManhattanDistance(B, WhitePosition)
                    possibleDirection = getPossibleDirection(B, WhitePosition)
                    for d in possibleDirection:
                        route = [WhitePosition, tuple(map(sum, zip(WhitePosition, d)))]
                        newNode = Node(black, white, route, huristicValue)
                        PriorityList.append(newNode)
                        newNode.cost += 1
                        if isKilled(newNode, B):
                            totalRoute.append(newNode.route)
                            Target = newNode
                            newNode.black.remove(B)
                            break
                        else:
                            PriorityList.append(newNode)
            PriorityList = [].append(Target)

        print(Target.route)








