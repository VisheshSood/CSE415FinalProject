import random

REPORTING = True

class MDP:
    def __init__(self):
        self.known_states = set()
        self.succ = {} # hash of adjacency lists by state.

    def register_start_state(self, start_state):
        self.start_state = start_state
        self.known_states.add(start_state)

    def register_actions(self, action_list):
        self.actions = action_list

    def register_operators(self, op_list):
        self.ops = op_list

    def register_transition_function(self, transition_function):
        self.T = transition_function

    def register_reward_function(self, reward_function):
        self.R = reward_function

    def state_neighbors(self, state):
        '''Return a list of the successors of state.  First check
           in the hash self.succ for these.  If there is no list for
           this state, then construct and save it.
           And then return the neighbors.'''
        neighbors = self.succ.get(state, False)
        if neighbors==False:
            neighbors = [op.apply(state) for op in self.ops if op.is_applicable(state)]
            self.succ[state]=neighbors
            self.known_states.update(neighbors)
        return neighbors

    def random_episode(self, nsteps):
        self.current_state = self.start_state
        self.current_reward = 0.0
        for i in range(nsteps):
            self.take_action(random.choice(self.actions))
            if self.current_state == 'DEAD':
                print('Terminating at DEAD state.')
                break
        if REPORTING: print("Done with "+str(i)+" of random exploration.")

    def take_action(self, a):
        s = self.current_state
        neighbors = self.state_neighbors(s)
        threshold = 0.0
        rnd = random.uniform(0.0, 1.0)
        r = 0
        for sp in neighbors:
            threshold += self.T(s, a, sp)
            if threshold>rnd:
                r = self.R(s, a, sp)
                break
        self.current_state = sp
        #if REPORTING: print("After action "+a+", moving to state "+str(sp)+\
        #                    "; reward is "+str(r))

    def generateAllStates(self):
        self.IterativeDFS(self.start_state)
        self.ending_states = []
        for state in self.known_states:
            if "DEAD" in self.succ.get(state):
                self.ending_states.append(state)
        self.indexOfEnd()
        print(self.known_states)

    def ValueIterations(self, discount, iterations):
        self.V = {}
        for state in self.known_states:
            self.V[state] = 0
        for n in range(iterations):
            new_V = {}
            for state in self.known_states:
                possible_values = []
                for action in self.actions:
                    value = 0
                    for successor in self.succ.get(state):
                        value += self.T(state, action, successor)*(self.R(state, action, successor) + discount * self.V.get(successor))
                    possible_values.append(value)
                max_value = max(possible_values)
                new_V[state] = max_value
            self.V = new_V

    def QLearning(self, discount, nEpisodes, epsilon):
        self.QValues = {}
        self.N = {}
        # initialize QValues to 0:
        for state in self.known_states:
            for action in self.actions:
                self.QValues[(state, action)] = 0
                self.N[(state, action)] = 0
        for i in range(nEpisodes):
            self.current_state = self.start_state
            while self.current_state != "DEAD":
                s = self.current_state
                a = self.decideAction(s, epsilon)
                self.N[(s, a)] += 1
                self.QValues[(s, a)] = self.Q(s, a, discount, epsilon)


    def alpha(self, state, action):
        return 1 / self.N.get((state, action))

    def getMaxAction(self, state):
        max_action = ""
        max = -10000
        for action in self.actions:
            action_val = self.QValues.get((state, action))
            if max < action_val:
                max = action_val
                max_action = action
        return max_action

    def Q(self, s, a, discount, epsilon):
        QVal = self.QValues.get((s, a))
        alpha = self.alpha(s, a)
        self.take_action(a)
        sp = self.current_state
        sp_max_action = self.getMaxAction(sp)
        T = self.T(s, a, sp)
        sample = self.R(s, a, sp) + discount * self.QValues.get((sp, sp_max_action))
        value = (1 - alpha) * QVal + alpha * sample
        if T == 0:
            self.current_state = s
            value = QVal
        return value

    def decideAction(self, state, epsilon):
        rnd = random.uniform(0.0, 1.0)
        if state in self.ending_states:
            return self.actions[self.index_of_end]
        if rnd < epsilon:
            action_num = random.randint(0, 4)
            return self.actions[action_num]
        else:
            return self.getMaxAction(state)

    def extractPolicy(self):
        self.optPolicy = {}
        for state in self.known_states:
            if state in self.ending_states:
                max_action = self.actions[4]
            else:
                max_action = self.getMaxAction(state)
            self.optPolicy[state] = max_action

    def indexOfEnd(self):
        for i in range(len(self.actions)):
            if self.actions[i] == 'End':
                self.index_of_end = i

    def IterativeDFS(self, initial_state):
        OPEN = [initial_state]
        CLOSED = []

        while OPEN != []:
            S = OPEN[0]
            del OPEN[0]
            CLOSED.append(S)
            L = self.state_neighbors(S)
            for state in L:
               if state not in CLOSED:
                   OPEN.append(state)

    def checkSuccessors(self):
        for state in self.known_states:
            print("Successors to ", state, ": ",self.succ.get(state))
