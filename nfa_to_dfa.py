import nfa as nfa
from graphviz import Digraph


class NFA:
    def __init__(self, num_states, states, num_alphabets, alphabets, start,
                 num_final_states, finals, num_transitions, transitions):
        self.num_states = num_states
        self.states = states
        self.num_alphabets = num_alphabets
        self.alphabets = alphabets
        self.alphabets.append('e')
        self.num_alphabets += 1
        self.start = start
        self.num_final_states = num_final_states
        self.finals = finals
        self.num_transitions = num_transitions
        self.transitions = transitions
        self.graph = Digraph()

        self.state_index_dict = dict()
        for i in range(self.num_states):
            self.state_index_dict[self.states[i]] = i
        self.alphabet_index_dict = dict()
        for i in range(self.num_alphabets):
            self.alphabet_index_dict[self.alphabets[i]] = i

        self.state_transition_dict = dict()
        for i in range(self.num_states):
            for j in range(self.num_alphabets):
                self.state_transition_dict[str(i) + str(j)] = []
        for i in range(self.num_transitions):
            self.state_transition_dict[str(self.state_index_dict[self.transitions[i][0]])
                                  + str(self.alphabet_index_dict[
                                            self.transitions[i][1]])].append(
                self.state_index_dict[self.transitions[i][2]])

    # Method to get input from User
    @classmethod
    def fromUser(cls):
        num_states = int(input("Number of States : "))
        states = list(input("States : ").split())
        num_alphabets = int(input("Number of Alphabets : "))
        alphabets = list(input("Alphabets : ").split())
        start = input("Start State : ")
        num_final_states = int(input("Number of Final States : "))
        finals = list(input("Final States : ").split())
        num_transitions = int(input("Number of Transitions : "))
        transitions = list()
        print("Enter Transitions (from alphabet to) (e for epsilon): ")
        for i in range(num_transitions):
            transitions.append(input("-> ").split())
        return cls(num_states, states, num_alphabets, alphabets, start,
                   num_final_states, finals, num_transitions, transitions)

    # Method to represent quintuple
    def __repr__(self):
        return "Q : " + str(self.states) + "\nΣ : "
        + str(self.alphabets) + "\nq0 : "
        + str(self.start) + "\nF : " + str(self.finals) + \
        "\nδ : \n" + str(self.state_transition_dict)

    def getEpsilonClosure(self, state):

        closure = dict()
        closure[self.state_index_dict[state]] = 0
        closure_stack = [self.state_index_dict[state]]

        while (len(closure_stack) > 0):

            cur = closure_stack.pop(0)

            for x in self.state_transition_dict[
                str(cur) + str(self.alphabet_index_dict['e'])]:
                if x not in closure.keys():
                    closure[x] = 0
                    closure_stack.append(x)
            closure[cur] = 1
        return closure.keys()

    def getStateName(self, state_list):

        name = ''
        for x in state_list:
            name += self.states[x]
        return name

    def isFinalDFA(self, state_list):


        for x in state_list:
            for y in self.finals:
                if (x == self.state_index_dict[y]):
                    return True
        return False


print("NFA to DFA")

nfa = NFA.fromUser()

nfa.graph = Digraph()


for x in nfa.states:
    if (x not in nfa.finals):
        nfa.graph.attr('node', shape='circle')
        nfa.graph.node(x)
    else:
        nfa.graph.attr('node', shape='doublecircle')
        nfa.graph.node(x)

nfa.graph.attr('node', shape='none')
nfa.graph.node('')
nfa.graph.edge('', nfa.start)

for x in nfa.transitions:
    nfa.graph.edge(x[0], x[2], label=('ε', x[1])[x[1] != 'e'])

nfa.graph.render('nfa', view=True)
dfa = Digraph()

epsilon_closure = dict()
for x in nfa.states:
    epsilon_closure[x] = list(nfa.getEpsilonClosure(x))

dfa_stack = list()
dfa_stack.append(epsilon_closure[nfa.start])

if (nfa.isFinalDFA(dfa_stack[0])):
    dfa.attr('node', shape='doublecircle')
else:
    dfa.attr('node', shape='circle')
dfa.node(nfa.getStateName(dfa_stack[0]))

dfa.attr('node', shape='none')
dfa.node('')
dfa.edge('', nfa.getStateName(dfa_stack[0]))
visited_dfa_states = list()
visited_dfa_states.append(epsilon_closure[nfa.start])


while (len(dfa_stack) > 0):
    cur_state = dfa_stack.pop(0)
    for al in range((nfa.num_alphabets) - 1):
        from_closure = set()
        for x in cur_state:
            from_closure.update(
                set(nfa.state_transition_dict[str(x) + str(al)]))

        if (len(from_closure) > 0):
            destination_states = set()
            for x in list(from_closure):
                destination_states.update(set(epsilon_closure[nfa.states[x]]))

            if list(destination_states) not in visited_dfa_states:
                dfa_stack.append(list(destination_states))
                visited_dfa_states.append(list(destination_states))

                if (nfa.isFinalDFA(list(destination_states))):
                    dfa.attr('node', shape='doublecircle')
                else:
                    dfa.attr('node', shape='circle')
                dfa.node(nfa.getStateName(list(destination_states)))

            dfa.edge(nfa.getStateName(cur_state),
                     nfa.getStateName(list(destination_states)),
                     label=nfa.alphabets[al])

        else:

            if (-1) not in visited_dfa_states:
                dfa.attr('node', shape='circle')
                dfa.node('Dead')

                for alpha in range(nfa.num_alphabets - 1):
                    dfa.edge('Dead', 'Dead', nfa.alphabets[alpha])


                visited_dfa_states.append(-1)

            dfa.edge(nfa.getStateName(cur_state, ),
                     'Dead', label=nfa.alphabets[al])


dfa.render('dfa', view=True)