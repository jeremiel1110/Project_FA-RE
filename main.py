with open('text_automata.txt', 'r') as file:
    text = file.read()
    print(text)


class FA:
    def __init__(self, alphabet_size, nb_states, initial_states, final_states, nb_transitions, transitions):
        self.alphabet_size = alphabet_size
        self.nb_states = nb_states
        self.initial_states = initial_states
        self.final_states = final_states
        self.nb_transitions = nb_transitions
        self.transitions = transitions

FA1 = FA(0, 0, [], [], 0, [])