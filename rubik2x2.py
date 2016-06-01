import copy
import random

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
INITIAL_STATE = [[2, 2, 0, 0], [1, 1, 3, 3], [2, 2, 0, 0], [3, 3, 1, 1], [5, 4, 5, 4], [4, 5, 4, 5]]
INT_TO_COLORS = {0: 'G', 1: 'O', 2: 'B', 3: 'R', 4: 'Y', 5: 'W',}
ACTIONS = ["Up", "Down", "Left", "Right", "Front", "Back"]
GOAL_STATE = None
OPERATORS = []


class Operator:
    def __init__(self, name, state_transf):
        self.name = name
        self.state_transf = state_transf

    def apply(self, s):
        return self.state_transf(s)


def createInitialState():
    global INITIAL_STATE
    createGoalState()
    createOperators()
    requestColors = input("Would you like to customize the colors of your Rubik's Cube? (y/n) ")
    if requestColors is 'y':
        resetInitialStateColors()
        getUserColors()
    return INITIAL_STATE

def resetInitialStateColors():
    global INT_TO_COLORS
    for i in range(6):
        INT_TO_COLORS[i] = None

def getUserColors():
    global INT_TO_COLORS
    for i in range(6):
        color = input("Please Enter Color " + str(i+1) + ": ").upper()
        while checkIfColorExists(color[0]):
            print("The color has initials that already exist")
            color = input("Please Enter Color " + str(i + 1) + ": ").upper()
        INT_TO_COLORS[i] = color[0]


def checkIfColorExists(char):
    global INT_TO_COLORS
    for i in range(6):
        if INT_TO_COLORS[i] == char:
            return True
    return False

def scramble():
    state = None
    for i in range (100):
        value = random.randint(0,5)
        state = OPERATORS[value].apply(INITIAL_STATE)
    return state



def deepEquals(state1, state2):
    for side in range(6):
        for tile in range(4):
            if state1[side][tile] != state2[side][tile]:
                return False
    return True


def hashCode(state):
    return str(state)


def copyState(state):
    return copy.deepcopy(state)


def createGoalState():
    global GOAL_STATE
    state = []
    for i in range(6):
        new = []
        for j in range(4):
            new.append(i)
        state.append(new)
    GOAL_STATE = state


def goalTest(s):
    for side in s:
        if len(set(side)) > 1:
            return False
    return True


def goalMessage():
    print("The Rubik's Cube has been solved!!")
    print("Final State: ")
    describeState(GOAL_STATE)


def describeState(state):
    global INT_TO_COLORS
    tiles = state[4]
    print("         -------")
    for i in range(0, 4, 2):
        print("        | " + INT_TO_COLORS.get(tiles[i]) + " | " + INT_TO_COLORS.get(tiles[i + 1]) + " | ")
    print("---------------------------------")
    for i in range(0, 4, 2):
        line = "| "
        line += INT_TO_COLORS.get(state[0][i]) + " | " + INT_TO_COLORS.get(state[0][i + 1]) + " | "
        line += INT_TO_COLORS.get(state[1][i]) + " | " + INT_TO_COLORS.get(state[1][i + 1]) + " | "
        line += INT_TO_COLORS.get(state[2][i]) + " | " + INT_TO_COLORS.get(state[2][i + 1]) + " | "
        line += INT_TO_COLORS.get(state[3][i]) + " | " + INT_TO_COLORS.get(state[3][i + 1]) + " | "
        print(line)
    tiles = state[5]
    print("---------------------------------")
    for i in range(0, 4, 2):
        print("        | " + INT_TO_COLORS.get(tiles[i]) + " | " +  INT_TO_COLORS.get(tiles[i + 1]) + " | ")

    print("         -------")

# going from 5 to 3, reverse order of tiles
# reverse back when going
def left(state):
    s = copyState(state)

    indices = [0, 1, 2]
    rotation = [5, 3, 4, 1]
    last_update = [s[1][0], s[1][2]]
    for i in range(3, 0, -1):
        if rotation[i] == 3:
            s[rotation[i]][3] = s[rotation[i - 1]][0]
            s[rotation[i]][1] = s[rotation[i - 1]][2]
        elif rotation[i] == 4:
            s[rotation[i]][0] = s[rotation[i - 1]][3]
            s[rotation[i]][2] = s[rotation[i - 1]][1]
        else:
            s[rotation[i]][0] = s[rotation[i - 1]][0]
            s[rotation[i]][2] = s[rotation[i - 1]][2]
    s[5][0] = last_update[0]
    s[5][2] = last_update[1]

    temp = s[0][0]
    s[0][0] = s[0][2]
    s[0][2] = s[0][3]
    s[0][3] = s[0][1]
    s[0][1] = temp
    return s


def right(state):
    s = copyState(state)

    indices = [0, 1, 2]
    rotation = [4, 3, 5, 1]
    last_update = [s[1][1], s[1][3]]
    for i in range(3, 0, -1):
        if rotation[i] == 3:
            s[rotation[i]][2] = s[rotation[i - 1]][1]
            s[rotation[i]][0] = s[rotation[i - 1]][3]
        elif rotation[i] == 5:
            s[rotation[i]][1] = s[rotation[i - 1]][2]
            s[rotation[i]][3] = s[rotation[i - 1]][0]
        else:
            s[rotation[i]][1] = s[rotation[i - 1]][1]
            s[rotation[i]][3] = s[rotation[i - 1]][3]
    s[4][1] = last_update[0]
    s[4][3] = last_update[1]

    temp = s[2][0]
    s[2][0] = s[2][2]
    s[2][2] = s[2][3]
    s[2][3] = s[2][1]
    s[2][1] = temp
    return s

def up(state):
    s = copyState(state)
    indices = [0, 1, 2]
    rotation = [3, 2, 1, 0]
    last_update = [s[0][0], s[0][1]]
    for i in range(3, 0, -1):
        s[rotation[i]][0] = s[rotation[i - 1]][0]
        s[rotation[i]][1] = s[rotation[i - 1]][1]
    s[3][0] = last_update[0]
    s[3][1] = last_update[1]
    temp = s[4][0]
    s[4][0] = s[4][2]
    s[4][2] = s[4][3]
    s[4][3] = s[4][1]
    s[4][1] = temp
    return s



def down(state):
    s = copyState(state)
    rotation = [1, 2, 3, 0]
    last_update = [s[0][2], s[0][3]]
    for i in range(3, 0, -1):
        s[rotation[i]][2] = s[rotation[i - 1]][2]
        s[rotation[i]][3] = s[rotation[i - 1]][3]
    s[1][2] = last_update[0]
    s[1][3] = last_update[1]
    temp = s[5][0]
    s[5][0] = s[5][2]
    s[5][2] = s[5][3]
    s[5][3] = s[5][1]
    s[5][1] = temp
    return s


def front(state):
    s = copyState(state)
    last_update = [s[5][0], s[5][1]]

    temp = s[1][0]
    s[1][0] = s[1][2]
    s[1][2] = s[1][3]
    s[1][3] = s[1][1]
    s[1][1] = temp



    # Get values from 2 and put into 5
    s[5][0] = s[2][2]
    s[5][1] = s[2][0]

    # Get values from 4 and put into 2
    s[2][0] = s[4][2]
    s[2][2] = s[4][3]

    # Get values from 0 and put into 4
    s[4][3] = s[0][1]
    s[4][2] = s[0][3]

    # Get values from 5 and put into 0
    s[0][1] = last_update[0]
    s[0][3] = last_update[1]

    return s

def back(state):
    s = copyState(state)
    last_update = [s[4][0], s[4][1]]


    temp = s[3][0]
    s[3][0] = s[3][2]
    s[3][2] = s[3][3]
    s[3][3] = s[3][1]
    s[3][1] = temp

    # 2 go to 4
    s[4][0] = s[2][1]
    s[4][1] = s[2][3]

    # 5 goes to 2
    s[2][1] = s[5][3]
    s[2][3] = s[5][2]

    # 0 goes to 5
    s[5][2] = s[0][0]
    s[5][3] = s[0][2]

    # 4 goes to 0

    s[0][0] = last_update[1]
    s[0][2] = last_update[0]

    return s



def h_side(s):
    value = 0
    for tile in s[0]:
        if tile == 0:
            value += 1
    for tile in s[1]:
        if tile == 1:
            value += 1
    for tile in s[2]:
        if tile == 2:
            value += 1
    for tile in s[3]:
        if tile == 3:
            value += 1
    for tile in s[4]:
        if tile == 4:
            value += 1
    for tile in s[5]:
        if tile == 5:
            value += 1

    return value


def h_none(s):
    return 0

def h_layer(s):
    value = 0
    for tile in s[5]:
        if tile == 5:
            value += 1

    greenList = s[0][-3:]
    orangeList = s[1][-3:]
    blueList = s[2][-3:]
    redList = s[3][-3:]

    count = 0
    for val in greenList:
        if val == 0:
            value += 1
            count += 1

    if count == 3:
        value += 3

    count = 0
    for val in orangeList:
        if val == 1:
            value += 1
            count += 1

    if count == 3:
        value += 3

    count = 0
    for val in blueList:
        if val == 2:
            value += 1
            count += 1

    if count == 3:
        value += 3

    count = 0
    for val in redList:
        if val == 3:
            value += 1
            count += 1

    if count == 3:
        value += 3

    for tile in s[4]:
        if tile == 4:
            value += 1

    return value


def createOperators():
    global OPERATORS
    operators = OPERATORS
    operators.append(Operator("Rotate Up", lambda s: up(up(s))))
    operators.append(Operator("Rotate Down", lambda s: down(down(s))))
    operators.append(Operator("Rotate Left", lambda s: left(left(s))))
    operators.append(Operator("Rotate Right", lambda s: right(right(s))))
    operators.append(Operator("Rotate Front", lambda s: front(front(s))))
    operators.append(Operator("Rotate Back", lambda s: back(back(s))))



HEURISTICS = {'h_layer': h_layer, 'h_side': h_side, 'h_none':h_none}

def T(s, a, sp):
    return 1

def R(s, a, sp):
    global GOAL_STATE
    if sp == GOAL_STATE:
        return 1
    else:
        return -0.01


import MDP

def test():
    '''Create the MDP, then run an episode of random actions for 10 steps.'''
    grid_MDP = MDP.MDP()
    grid_MDP.register_start_state(createInitialState())
    grid_MDP.register_goal_state(GOAL_STATE)
    grid_MDP.register_actions(ACTIONS)
    grid_MDP.register_operators(OPERATORS)
    grid_MDP.register_transition_function(T)
    grid_MDP.register_reward_function(R)
    grid_MDP.generateAllStates()
    grid_MDP.random_episode(10)
    #grid_MDP.ValueIterations(.8, 10)
    #printGrids(grid_MDP.V)
    #grid_MDP.checkSuccessors()
    #grid_MDP.QLearning(0.8, 3, 0.2)
    # displayQValues(grid_MDP)
    # displayOptimalPolicy(grid_MDP)


#createGoalState()
#createInitialState()
#print((right(right(back(back(front(front(up(up(GOAL_STATE))))))))))
#
#describeState(INITIAL_STATE)
# print()
#describeState(GOAL_STATE)
# print()
# describeState(left(left(GOAL_STATE)))
# createOperators()
# print()
# print()
# describeState(OPERATORS[1].apply(INITIAL_STATE))
# print()
# describeState(OPERATORS[2].apply(INITIAL_STATE))
# print()
# describeState(OPERATORS[3].apply(INITIAL_STATE))
# print(str(INITIAL_STATE[2][-3:]))
#
