import copy

# <METADATA>
QUIET_VERSION = "0.1"
PROBLEM_NAME = "Rubik Cube Solver"
PROBLEM_VERSION = "0.1"
PROBLEM_AUTHORS = ['V. Sood', 'J. Chavez']
PROBLEM_CREATION_DATE = "28-MAY-2016"
PROBLEM_DESC = \
    '''
    This formulation of the Rubik's Cube uses generic
    Python 3 constructs and has been tested with Python 3.4.
    It is designed to work according to the QUIET tools interface.
    '''
# </METADATA>

# SIDES = ["Left", "Front", "Right", "Back", "Up", "Down"]
INITIAL_STATE = [[5, 2, 5, 2, 1, 1, 2, 1, 1], [3, 3, 4, 5, 2, 5, 5, 3, 5],
                 [6, 4, 6, 3, 3, 4, 3, 3, 4], [2, 1, 1, 6, 4, 6, 6, 1, 6],
                 [4, 4, 3, 5, 5, 5, 4, 4, 1], [2, 6, 2, 2, 6, 2, 3, 6, 3]]
GOAL_STATE = None


class Operator:
    def __init__(self, name, state_transf):
        self.name = name
        self.state_transf = state_transf

    def apply(self, s):
        return self.state_transf(s)


def deepEquals(state1, state2):
    for side in range(6):
        for tile in range(9):
            if state1[side][tile] != state2[side][tile]:
                return False
    return True


def hashcode(state):
    return str(GOAL_STATE)


def copyState(state):
    return copy.deepcopy(state)


def createGoalState():
    global GOAL_STATE
    state = []
    for i in range(6):
        new = []
        for j in range(9):
            new.append(i + 1)
        state.append(new)
    GOAL_STATE = state


def goalMessage():
    print("The Rubik's Cube has been solved!!")
    print("Final State: ")
    describeState(GOAL_STATE)


def describeState(state):
    tiles = state[4]
    for i in range(0, 9, 3):
        print("      " + str(tiles[i]) + " " + str(tiles[i + 1]) + " " + str(tiles[i + 2]))

    for i in range(0, 9, 3):
        line = ""
        line += str(state[0][i]) + " " + str(state[0][i + 1]) + " " + str(state[0][i + 2]) + " "
        line += str(state[1][i]) + " " + str(state[1][i + 1]) + " " + str(state[1][i + 2]) + " "
        line += str(state[2][i]) + " " + str(state[2][i + 1]) + " " + str(state[2][i + 2]) + " "
        line += str(state[3][i]) + " " + str(state[3][i + 1]) + " " + str(state[3][i + 2]) + " "
        print(line)
    tiles = state[5]

    for i in range(0, 9, 3):
        print("      " + str(tiles[i]) + " " + str(tiles[i + 1]) + " " + str(tiles[i + 2]))


def scramble():
    return None


def move(action, s):
    # act = actions.get(action)
    act(s)


# going from 5 to 3, reverse order of tiles
# reverse back when going
def left(s):
    indices = [0, 1, 2]
    rotation = [5, 3, 4, 1]
    last_update = [s[1][0], s[1][3], s[1][6]]
    for i in range(3, 0, -1):
        if rotation[i] == 3:
            s[rotation[i]][8] = s[rotation[i - 1]][0]
            s[rotation[i]][5] = s[rotation[i - 1]][3]
            s[rotation[i]][2] = s[rotation[i - 1]][6]
        if rotation[i] == 4:
            s[rotation[i]][0] = s[rotation[i - 1]][8]
            s[rotation[i]][3] = s[rotation[i - 1]][5]
            s[rotation[i]][6] = s[rotation[i - 1]][2]
        else:
            s[rotation[i]][0] = s[rotation[i - 1]][0]
            s[rotation[i]][3] = s[rotation[i - 1]][3]
            s[rotation[i]][6] = s[rotation[i - 1]][6]
    s[5][0] = last_update[0]
    s[5][3] = last_update[1]
    s[5][6] = last_update[2]
    return s


def right(s):
    indices = [0, 1, 2]
    rotation = [4, 3, 5, 1]
    last_update = [s[1][2], s[1][5], s[1][8]]
    for i in range(3, 0, -1):
        if rotation[i] == 3:
            s[rotation[i]][6] = s[rotation[i - 1]][2]
            s[rotation[i]][3] = s[rotation[i - 1]][5]
            s[rotation[i]][0] = s[rotation[i - 1]][8]
        if rotation[i] == 5:
            s[rotation[i]][2] = s[rotation[i - 1]][6]
            s[rotation[i]][5] = s[rotation[i - 1]][3]
            s[rotation[i]][8] = s[rotation[i - 1]][0]
        else:
            s[rotation[i]][2] = s[rotation[i - 1]][2]
            s[rotation[i]][5] = s[rotation[i - 1]][5]
            s[rotation[i]][8] = s[rotation[i - 1]][8]
    s[4][2] = last_update[0]
    s[4][5] = last_update[1]
    s[4][8] = last_update[2]
    return s


def up(s):
    indices = [0, 1, 2]
    rotation = [3, 2, 1, 0]
    last_update = [s[0][0], s[0][1], s[0][2]]
    for i in range(3, 0, -1):
        s[rotation[i]][0] = s[rotation[i - 1]][0]
        s[rotation[i]][1] = s[rotation[i - 1]][1]
        s[rotation[i]][2] = s[rotation[i - 1]][2]
    s[3][0] = last_update[0]
    s[3][1] = last_update[1]
    s[3][2] = last_update[2]
    return s


def down(s):
    indices = [6, 7, 8]
    rotation = [1, 2, 3, 0]
    last_update = [s[0][6], s[0][7], s[0][8]]
    for i in range(3, 0, -1):
        s[rotation[i]][6] = s[rotation[i - 1]][6]
        s[rotation[i]][7] = s[rotation[i - 1]][7]
        s[rotation[i]][8] = s[rotation[i - 1]][8]
    s[1][6] = last_update[0]
    s[1][7] = last_update[1]
    s[1][8] = last_update[2]
    return s


def front(s):
    last_update = [s[5][0], s[5][1], s[5][2]]

    # Get values from 2 and put into 5
    s[5][0] = s[2][6]
    s[5][1] = s[2][3]
    s[5][2] = s[2][0]

    # Get values from 4 and put into 2
    s[2][0] = s[4][6]
    s[2][3] = s[4][7]
    s[2][6] = s[4][8]

    # Get values from 0 and put into 4
    s[4][8] = s[0][2]
    s[4][7] = s[0][5]
    s[4][6] = s[0][8]

    # Get values from 5 and put into 0
    s[0][2] = last_update[0]
    s[0][5] = last_update[1]
    s[0][8] = last_update[2]

    tempArray = []

    for i in range(3):
        val1 = s[1][i * 3]
        val2 = s[1][(i * 3) + 1]
        val3 = s[1][(i * 3) + 2]
        tempArray.append([val1, val2, val3])

    rot2(tempArray)

    list_to_update = []
    for i in range(3):
        for j in range(3):
            list_to_update.append(tempArray[i][j])

    s[1] = list_to_update

    return s


def rot2(a):
    n = 3
    c = (n + 1) / 2
    f = n / 2
    for x in range(2):
        for y in range(1):
            a[x][y] = a[x][y] ^ a[n - 1 - y][x]
            a[n - 1 - y][x] = a[x][y] ^ a[n - 1 - y][x]
            a[x][y] = a[x][y] ^ a[n - 1 - y][x]

            a[n - 1 - y][x] = a[n - 1 - y][x] ^ a[n - 1 - x][n - 1 - y]
            a[n - 1 - x][n - 1 - y] = a[n - 1 - y][x] ^ a[n - 1 - x][n - 1 - y]
            a[n - 1 - y][x] = a[n - 1 - y][x] ^ a[n - 1 - x][n - 1 - y]

            a[n - 1 - x][n - 1 - y] = a[n - 1 - x][n - 1 - y] ^ a[y][n - 1 - x]
            a[y][n - 1 - x] = a[n - 1 - x][n - 1 - y] ^ a[y][n - 1 - x]
            a[n - 1 - x][n - 1 - y] = a[n - 1 - x][n - 1 - y] ^ a[y][n - 1 - x]


def back(s):
    return 0


createGoalState()
describeState(INITIAL_STATE)
print()
describeState(front(INITIAL_STATE))



