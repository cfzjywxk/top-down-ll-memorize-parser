from os import popen
import time
__author__ = 'ray'

class FiniteAutomaton:
    @staticmethod
    def epsilon():
        return ":e:"

    def __init__(self):
        self.states = set()
        self.start_state = None
        self.finish_states = set()
        self.transition_dict = dict()
        self.language = set()

    def set_start_state(self, start_state):
        self.start_state = start_state
        self.states.add(start_state)

    def add_final_states(self, to_add_states):
        if isinstance(to_add_states, int):
            to_add_states = [to_add_states]
        for to_add_state in to_add_states:
            self.finish_states.add(to_add_state)
        self.states.union(self.finish_states)

    def add_transitions(self, from_state, to_state, paths):
        if isinstance(paths, str):
            paths = set([paths])
        if self.transition_dict.has_key(from_state):
            if self.transition_dict[from_state].has_key(to_state):
                self.transition_dict[from_state][to_state].union(paths)
            else:
                self.transition_dict[from_state][to_state] = paths
        else:
            self.transition_dict[from_state] = {to_state : paths}
        self.states.add(from_state)
        self.states.add(to_state)
        for key in paths:
            self.language.add(key)

    def get_transitions(self, from_states, key):
        if isinstance(from_states, int):
            from_states = [from_states]
        ret_states = set()
        for from_st in from_states:
            if from_st in self.transition_dict:
                for dest_st in self.transition_dict[from_st]:
                    if key in self.transition_dict[from_st][dest_st]:
                        ret_states.add(dest_st)
        return ret_states

    def get_e_close(self, t_states):
        ret_states = set()
        t_states = set([t_states])
        while len(t_states) != 0:
            cur_state = t_states.pop()
            ret_states.add(cur_state)
            if cur_state in self.transition_dict:
                for state in self.transition_dict[cur_state]:
                    if FiniteAutomaton.epsilon() in self.transition_dict[cur_state][state] and state not in ret_states:
                        t_states.add(state) #continue on :e: transfer!
        return ret_states

    def display(self):
        print "states:", self.states
        print "start state: ", self.start_state
        print "final states:", self.finish_states
        print "transitions:"
        for fromstate, tostates in self.transition_dict.items():
            for state in tostates:
                for char in tostates[state]:
                    print "  ",fromstate, "->", state, "on '"+char+"'",
            print

    def get_print_Text(self):
        text = "language: {" + ", ".join(self.language) + "}\n"
        text += "states: {" + ", ".join(map(str, self.states)) + "}\n"
        text += "start state: " + str(self.start_state) + "\n"
        text += "final states: {" + ", ".join(map(str,self.finish_states)) + "}\n"
        text += "transitions:\n"
        linecount = 5
        for fromstate, tostates in self.transition_dict.items():
            for state in tostates:
                for char in tostates[state]:
                    text += "    " + str(fromstate) + " -> " + str(state) + " on '" + char + "'\n"
                    linecount +=1
        return [text, linecount]

    #generate dotFile content
    def getDotFile(self):
        dotFile = "digraph DFA {\nrankdir=LR\n"
        if len(self.states) != 0:
            dotFile += "root=s1\nstart [shape=point]\nstart->s%d\n" % self.start_state
            for state in self.states:
                if state in self.finish_states:
                    dotFile += "s%d [shape=doublecircle]\n" % state
                else:
                    dotFile += "s%d [shape=circle]\n" % state
            for fromstate, tostates in self.transition_dict.items():
                for state in tostates:
                    for char in tostates[state]:
                        dotFile += 's%d->s%d [label="%s"]\n' % (fromstate, state, char)
        dotFile += "}"
        return dotFile

class nfa_to_dfa:
    @staticmethod
    def get_dfa_from_nfa(nfa):
        #start from start state e-closure
        allstates = dict()
        eclose = dict()
        count = 1
        state1 = nfa.get_e_close(nfa.start_state)
        eclose[nfa.start_state] = state1
        dfa = FiniteAutomaton()
        dfa.set_start_state(count)
        states = [[state1, count]]
        allstates[count] = state1
        count +=  1
        dfa.language = dfa.language.union(nfa.language)
        while len(states) != 0:
            [state, fromindex] = states.pop()
            for char in dfa.language:
                if char == FiniteAutomaton.epsilon():
                    continue
                #get the eclose states from a 'states set' on path char
                trstates = nfa.get_transitions(state, char)
                for s in list(trstates)[:]:
                    if s not in eclose:
                        eclose[s] = nfa.get_e_close(s)
                    trstates = trstates.union(eclose[s])
                if len(trstates) != 0:
                    if trstates not in allstates.values():
                        states.append([trstates, count])
                        allstates[count] = trstates
                        toindex = count
                        count +=  1
                    else:
                        toindex = [k for k, v in allstates.iteritems() if v  ==  trstates][0]
                    dfa.add_transitions(fromindex, toindex, char)
        #set the final states in dfa
        for value, state in allstates.iteritems():
            for f_state in nfa.finish_states:
                if f_state in state:
                    dfa.add_final_states(value)
        dfa.language.remove(FiniteAutomaton.epsilon())
        return dfa

    #minimize the dfa Hopcroft algorithm
    @staticmethod
    def minimise_dfa(dfa):
        #debug dfa = FiniteAutomaton()
        #init return value
        mdfa = FiniteAutomaton()
        mdfa.language = mdfa.language.union(dfa.language)
        #start minize
        T = set()
        T.add(frozenset(dfa.finish_states))
        T.add(frozenset(dfa.states - dfa.finish_states))
        P = set()
        while P != T:
            P = T
            T = set()
            #init a dict to indicate where state from
            #do split operation on states set p
            state_from = dict()
            for pp in P:
                for state in pp:
                    state_from[state] = pp
            #try to split the state sets
            for p in P:
                s1 = set()
                s2 = set()
                is_splited = False
                ans_list = list()
                ans_dict = dict()
                for char in dfa.language:
                    ans_dict.clear()
                    ans_list = list()
                    state_list = []
                    #judge if char split set p
                    #if there is split, break out the loop and adjust T set
                    if len(p) != 1:
                        state_to_set = dict() #what set the state will goto
                        for state in p:
                            t_states = dfa.get_transitions(state, char)
                            for t_state in t_states:
                                t_set = state_from[t_state]
                                if state not in state_to_set.keys():
                                    state_to_set[state] = set()
                                    state_to_set[state].add(frozenset(t_set))
                                else:
                                    state_to_set[state].add(frozenset(t_set))
                            state_list.append(state)
                        #loop every state, merge the same transfering
                        for cur_state in state_list:
                            if len(ans_list) == 0:
                                ans_list.append(cur_state)
                                ans_dict[cur_state] = set()
                                ans_dict[cur_state].add(cur_state)
                            else:
                                is_new_set = True
                                for t_stat in ans_list:
                                    if state_to_set[t_stat] == state_to_set[cur_state]:
                                        is_new_set = False
                                        ans_dict[t_stat].add(cur_state)
                                if is_new_set:
                                    ans_list.append(cur_state)
                                    ans_dict[cur_state] = set()
                                    ans_dict[cur_state].add(cur_state)
                        if len(ans_dict) != 1:
                            is_splited = True
                    if is_splited:
                        break
                if is_splited:
                    for k, v in ans_dict.items():
                        T.add(frozenset(v))
                else:
                    T.add(frozenset(p))
        #set the states and transitions
        idx_dict = dict()
        count = 1
        stat_dict = dict()
        for state_set in T:
            for state in state_set:
                stat_dict[state] = state_set
        for state_set in T:
            idx_dict[frozenset(state_set)] = count
            count += 1
        for char in mdfa.language:
            for state in dfa.states:
                t_states = dfa.get_transitions(state, char)
                for t_state in t_states:
                    from_idx = idx_dict[frozenset(stat_dict[state])]
                    to_idx = idx_dict[frozenset(stat_dict[t_state])]
                    mdfa.add_transitions(from_idx, to_idx, char)
        #set the start state
        s_idx = idx_dict[stat_dict[dfa.start_state]]
        mdfa.set_start_state(s_idx)
        #set the final states
        for e_state in dfa.finish_states:
            e_idx = idx_dict[stat_dict[e_state]]
            mdfa.add_final_states(e_idx)
        return mdfa

def drawGraph(automata, file = ""):
    f = popen(r"dot -Tpng -o graph%s.png" % file, 'w')
    try:
        f.write(automata.getDotFile())
    except:
        raise BaseException("Error creating graph")
    finally:
        f.close()

