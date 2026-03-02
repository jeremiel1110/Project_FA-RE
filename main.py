


def select_text_automata():
    available_automatas = [
        'text_automata.txt',
    ]
    selected = 'text_automata.txt'
    print("What automata do you want to choose ?")
    print("selected :",selected)
    for i in range(len(available_automatas)):
        print(i,".  ",available_automatas[i])
    selected = available_automatas[int(input())]
    return selected

def read_automata(selected):
    with open(selected, 'r') as file :
        text= file.read()
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

def FA_reader(filename:str) -> FA:
    with open(filename) as file:
        lines = [line.rstrip() for line in file]

    FA = FA(lines[0], lines[1], lines[2], lines[3], lines[4], lines[5:])

    return FA

    return text

def main():
    read_automata(select_text_automata())

    

main()