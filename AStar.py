import sys
import queue as Q
import importlib

Problem = importlib.import_module('rubik2x2')
heuristics = Problem.HEURISTICS['h_side']

print("\nWelcome to AStar")
COUNT = None
BACKLINKS = {}
BACKACTIONS = {}


def runAStar():
    initial_state = Problem.createInitialState()
    print("Initial State:")
    print(Problem.describeState(initial_state))
    global COUNT, BACKLINKS, BACKACTIONS
    COUNT = 0
    IterativeAStar(initial_state)
    print()
    print(str(COUNT) + " states examined.")


def IterativeAStar(initial_state):
    global COUNT, BACKLINKS, BACKACTIONS

    OPEN = Q.PriorityQueue()
    OPEN.put((heuristics(initial_state), initial_state))
    LIST = []
    LIST.append(initial_state)
    CLOSED = []
    BACKLINKS[Problem.hashCode(initial_state)] = -1
    BACKACTIONS[Problem.hashCode(initial_state)] = 'Start State'


    while LIST != []:
        S_tuple = OPEN.get()
        S = S_tuple[1]
        step = S_tuple[0] - heuristics(S)

        LIST.remove(S)
        CLOSED.append(S)

        if Problem.goalTest(S):
            Problem.goalMessage()
            print("COUNT = " + str(COUNT))
            print("len(OPEN)=" + str(len(LIST)))
            print("len(CLOSED)=" + str(len(CLOSED)))
            backtrace(S)
            return

        COUNT += 1
        #Problem.describeState(S)
        # print()
        if (COUNT % 32) == 0:
            print(".", end="")
            if (COUNT % 128) == 0:
                print()
                Problem.describeState(S)
                print("COUNT = " + str(COUNT))
                print("len(OPEN)=" + str(len(LIST)))
                print("len(CLOSED)=" + str(len(CLOSED)))

        L = []
        for op in Problem.OPERATORS:
            new_state = op.state_transf(S)
            if not occurs_in(new_state, CLOSED):
                L.append(new_state)
                BACKLINKS[Problem.hashCode(new_state)] = S
                BACKACTIONS[Problem.hashCode(new_state)] = op.name

        repeat = -1
        for i in range(len(L)):
            for j in range(len(LIST)):
                if Problem.deepEquals(L[i], LIST[j]):
                    repeat = i;
                    break
        if repeat != -1:
            del L[repeat]

        for s2 in L:
            OPEN.put((step + 1 + heuristics(s2), s2))

        LIST = LIST + L


def backtrace(S):
    global BACKLINKS, BACKACTIONS
    X = BACKACTIONS[Problem.hashCode(S)]
    path = []
    while not S == -1:
        tuple = (X,S)
        path.append(tuple)
        S = BACKLINKS[Problem.hashCode(S)]
        if S != -1:
            X = BACKACTIONS[Problem.hashCode(S)]
        else :
            X = 'Done!'
    path.reverse()
    print("Solution path: ")
    for s in path:
        print()
        print(s[0] + ':')
        print()
        Problem.describeState(s[1])

    return path


def occurs_in(s1, lst):
    for s2 in lst:
        if Problem.deepEquals(s1, s2): return True
    return False


if __name__ == '__main__':
    runAStar()
