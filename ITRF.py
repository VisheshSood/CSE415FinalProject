import sys

if sys.argv==[''] or len(sys.argv)<2:
  import rubik2x2 as Problem
else:
  import importlib
  Problem = importlib.import_module(sys.argv[1])


print("\nWelcome to ItrDFS")
COUNT = None
BACKLINKS = {}

def runDFS():
  initial_state = Problem.createInitialState()
  print("Initial State:")
  Problem.describeState(initial_state)
  global COUNT, BACKLINKS
  COUNT = 0
  BACKLINKS = {}
  IterativeDFS(initial_state)
  print(str(COUNT)+" states examined.")

def IterativeDFS(initial_state):
  global COUNT, BACKLINKS

  OPEN = [initial_state]
  CLOSED = []
  BACKLINKS[Problem.hashCode(initial_state)] = -1

  while OPEN != []:
    S = OPEN[0]
    del OPEN[0]
    CLOSED.append(S)

    if Problem.goalTest(S):
      Problem.goalMessage()
      backtrace(S)
      return

    COUNT += 1
    if (COUNT % 32)==0:
       print(".",end="")
       if (COUNT % 128)==0:
         print("COUNT = "+str(COUNT))
         print("len(OPEN)="+str(len(OPEN)))
         print("len(CLOSED)="+str(len(CLOSED)))
    L = []
    for op in Problem.OPERATORS:
      #Optionally uncomment the following when debugging
      #a new problem formulation.
      #print("Trying operator: "+op.name)
      new_state = op.state_transf(S)
      if not occurs_in(new_state, CLOSED):
        L.append(new_state)
        BACKLINKS[Problem.hashCode(new_state)] = S
      #Uncomment for debugging:
      #print(Problem.DESCRIBE_STATE(new_state))

    for s2 in L:
      for i in range(len(OPEN)):
        if Problem.deepEquals(s2, OPEN[i]):
          del OPEN[i]; break

    OPEN = L + OPEN

def backtrace(S):
  global BACKLINKS

  path = []
  while not S == -1:
    path.append(S)
    S = BACKLINKS[Problem.hashCode(S)]
  path.reverse()
  print("Solution path: ")
  for s in path:
    print(Problem.describeState(s))
  return path


def occurs_in(s1, lst):
  for s2 in lst:
    if Problem.deepEquals(s1, s2): return True
  return False

if __name__=='__main__':
  runDFS()
