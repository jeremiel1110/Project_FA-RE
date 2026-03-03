


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
    print("Transition table :")
    lowercase_alphabet = [chr(i) for i in range(ord('a'), ord('z') + 1)] #get alphabets character for links
    table = {str(i): {lowercase_alphabet[j]: [] for j in range(int(FA.alphabet_size))} for i in range(int(FA.nb_states))}
    #prints header line
    print("\t","\t","\t",end='')
    for i in range(int(FA.alphabet_size)): print("|","\t",lowercase_alphabet[i],"\t",end='')
    print("|")
    print("---------","-" * (16 * (int(FA.alphabet_size) + 1)))
    for i in range(int(FA.nb_states)):
        state_str = str(i)
        
        prefix = ""
        if state_str in map(str, FA.initial_states): prefix += "->"
        if state_str in map(str, FA.final_states): prefix += "<-"
        
        
        print(prefix, "\t", "|", "\t", state_str, end='\t') #affiche la 1ere cellulle a gauche avec état et fléche
        
        # Affichage des cellules pour chaque lettre
        for j in range(int(FA.alphabet_size)):
            lettre = lowercase_alphabet[j]
            targets = table[state_str][lettre]
            
            if not targets:
                cell_value = "--"
            else:
                cell_value = ",".join(targets)
            
            print("|", "\t", cell_value, "\t", end='')
        
        print("|") # Fin de ligne
    


    

def main():
    selected = select_text_automata()
    FA_used = FA_reader(selected)
    print_FA(FA_used)
    

main()