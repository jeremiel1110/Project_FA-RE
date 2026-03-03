def select_text_automata():
    automatas = ['text_automata.txt']
    selected = 'text_automata.txt'
    print("What automata do you want to choose ?")
    print("selected :",selected)

    for i in range(len(automatas)):
        print(i,".  ",automatas[i],"")

    selected = automatas[int(input())]
    return selected



class FA:
    def __init__(self, alphabet_size, nb_states, initial_states, final_states, nb_transitions, transitions):
        self.alphabet_size = alphabet_size
        self.nb_states = nb_states
        self.initial_states = initial_states
        self.final_states = final_states
        self.nb_transitions = nb_transitions
        self.transitions = transitions

    
    def Display_FA(self):
        print("Alphabet size :", self.alphabet_size)
        print("Number of states :", self.nb_states)
        print("Initial states :", self.initial_states)
        print("Final states :", self.final_states)
        print("Number of transitions :", self.nb_transitions)
        print("Transitions :")
        for transition in self.transitions:
            print(transition)



def FA_reader(selected:str) -> FA:
    with open(selected) as file:
        lines = [line.rstrip() for line in file]

    FA1 = FA(lines[0], lines[1], lines[2], lines[3], lines[4], lines[5:])
    return FA1


def main():
    selected = select_text_automata()
    FA_used = FA_reader(selected)
    FA_used.Display_FA()

main()
