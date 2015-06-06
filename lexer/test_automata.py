__author__ = 'ray'
from automata import FiniteAutomaton
from automata import drawGraph
from automata import nfa_to_dfa
#init a nfa
nfa = FiniteAutomaton()
nfa.add_transitions(0, 1, FiniteAutomaton.epsilon())
nfa.add_transitions(0, 7, FiniteAutomaton.epsilon())
nfa.add_transitions(1, 2, FiniteAutomaton.epsilon())
nfa.add_transitions(1, 4, FiniteAutomaton.epsilon())
nfa.add_transitions(2, 3, 'a')
nfa.add_transitions(4, 5, 'b')
nfa.add_transitions(3, 6, FiniteAutomaton.epsilon())
nfa.add_transitions(5, 6, FiniteAutomaton.epsilon())
nfa.add_transitions(6, 1, FiniteAutomaton.epsilon())
nfa.add_transitions(6, 7, FiniteAutomaton.epsilon())
nfa.add_transitions(7, 8, 'a')
nfa.add_transitions(8, 9, 'b')
nfa.add_transitions(9, 10, 'b')
nfa.set_start_state(0)
nfa.add_final_states(10)

drawGraph(nfa, 'test_nfa')
#convert nfa to dfa
dfa = nfa_to_dfa.get_dfa_from_nfa(nfa)
drawGraph(dfa, 'test_dfa')

#minize dfa
dfa = nfa_to_dfa.minimise_dfa(dfa)
drawGraph(dfa, 'minize_dfa')