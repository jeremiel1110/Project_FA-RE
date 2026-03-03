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
    def __init__(self, alphabet_size:int, nb_states:int, initial_states:tuple, final_states:tuple, nb_transitions:int, transitions:list):
        self.alphabet_size = alphabet_size
        self.nb_states = nb_states
        self.initial_states = initial_states
        self.final_states = final_states
        self.nb_transitions = nb_transitions
        self.transitions = transitions

    def import_FA(selected:str)->FA:
        pass

def main():
    selected = select_text_automata
    FiniteAutomaton = FA
    FiniteAutomaton.import_FA()

if __name__ == '__name__':
    main()