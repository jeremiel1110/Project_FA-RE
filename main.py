


def select_text_automata():
    available_automatas:list[str] = [
        'text_automata.txt',
    ]
    selected:str = 'text_automata.txt'
    print("What automata do you want to choose ?")
    print("selected :",selected)
    for i in range(len(available_automatas)):
        print(i,".  ",available_automatas[i])
    selected = available_automatas[int(input())]
    return selected




class FA:
    def __init__(self, alphabet_size, nb_states, initial_states, final_states, nb_transitions, transitions):
        self.alphabet_size = alphabet_size
        self.nb_states = nb_states
        self.initial_states = initial_states
        self.final_states = final_states
        self.nb_transitions = nb_transitions
        self.transitions = transitions

FA1 = FA(0, 0, [], [], 0, [])

def FA_reader(selected:str) -> FA:
    with open(selected) as file:
        lines = [line.rstrip() for line in file]

    FA1 = FA(lines[0], lines[1], lines[2], lines[3], lines[4], lines[5:])

    return FA1

def print_FA(FA:FA):
    print("Alphabet size :", FA.alphabet_size)
    print("Number of states :", FA.nb_states)
    print("Initial states :", FA.initial_states)
    print("Final states :", FA.final_states)
    print("Number of transitions :", FA.nb_transitions)
    print("Transitions :")
    for transition in FA.transitions:
        print(transition)

def main():
    selected = select_text_automata()
    FA_used = FA_reader(selected)
    print_FA(FA_used)
    

main()