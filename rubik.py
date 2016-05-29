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
                 [4, 4, 1, 5, 5, 5, 4, 4, 1], [2, 6, 2, 2, 6, 2, 3, 6, 3]]
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
            new.append(i+1)
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

createGoalState()
describeState(INITIAL_STATE)



