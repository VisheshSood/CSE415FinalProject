import sys
import queue as Q
import importlib

Problem = importlib.import_module('rubik')
heuristics = Problem.HEURISTICS['h_row']

print("\nWelcome to AStar")
COUNT = None
BACKLINKS = {}


def runAStar():
    initial_state = Problem.createInitialState()
    print("Initial State:")
    print(Problem.describeState(initial_state))
    global COUNT, BACKLINKS
    COUNT = 0
    BACKLINKS = {}
    IterativeAStar(initial_state)
    print(str(COUNT) + " states examined.")


def IterativeAStar(initial_state):
    global COUNT, BACKLINKS

    OPEN = Q.PriorityQueue()
    OPEN.put((heuristics(initial_state), initial_state))
    LIST = []
    LIST.append(initial_state)
    CLOSED = []
    BACKLINKS[Problem.HASHCODE(initial_state)] = -1

    while LIST != []:
        S_tuple = OPEN.get()
        S = S_tuple[1]
        step = S_tuple[0] - heuristics(S)

        LIST.remove(S)
        CLOSED.append(S)

        if Problem.GOAL_TEST(S):
            print(Problem.GOAL_MESSAGE_FUNCTION(S))
            print("COUNT = " + str(COUNT))
            print("len(OPEN)=" + str(len(LIST)))
            print("len(CLOSED)=" + str(len(CLOSED)))
            backtrace(S)
            return

        COUNT += 1
        if (COUNT % 32) == 0:
            print(".", end="")
            if (COUNT % 128) == 0:
                print("COUNT = " + str(COUNT))
                print("len(OPEN)=" + str(len(LIST)))
                print("len(CLOSED)=" + str(len(CLOSED)))

        L = []
        for op in Problem.OPERATORS:
            if op.precond(S):
                new_state = op.state_transf(S)
                if not occurs_in(new_state, CLOSED):
                    L.append(new_state)
                    BACKLINKS[Problem.HASHCODE(new_state)] = S

        repeat = -1
        for i in range(len(L)):
            for j in range(len(LIST)):
                if Problem.DEEP_EQUALS(L[i], LIST[j]):
                    repeat = i;
                    break
        if repeat != -1:
            del L[repeat]

        for s2 in L:
            OPEN.put((step + 1 + heuristics(s2), s2))

        LIST = LIST + L


def backtrace(S):
    global BACKLINKS

    path = []
    while not S == -1:
        path.append(S)
        S = BACKLINKS[Problem.HASHCODE(S)]
    path.reverse()
    print("Solution path: ")
    for s in path:
        print(Problem.DESCRIBE_STATE(s))
    return path


def occurs_in(s1, lst):
    for s2 in lst:
        if Problem.DEEP_EQUALS(s1, s2): return True
    return False


if __name__ == '__main__':
    runAStar()
