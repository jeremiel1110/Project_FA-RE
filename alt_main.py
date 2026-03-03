def select_text_automata():
    available_automatas:list[str] = ['text_automata.txt']
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

    def import_FA(selected:str)->"FA":
        with open(selected) as file:
            lines = [line.rstrip() for line in file]

        starting_states_list, final_states_list = [], []

        for character in lines[2][1:]:
            if character != " ":
                starting_states_list.append(int(character))

        for character in lines[3][1:]:
            if character != " ":
                final_states_list.append(int(character))

        imported_FA = FA(int(lines[0]), int(lines[1][0]), (int(lines[2][0]), starting_states_list), (int(lines[3][0]), final_states_list), int(lines[4]), lines[5:])
        return imported_FA
    
    def print_info(self:"FA"):
        print("Alphabet size :", self.alphabet_size)
        print("Number of states :", self.nb_states)
        print("Initial states :", self.initial_states)
        print("Final states :", self.final_states)
        print("Number of transitions :", self.nb_transitions)
        
    def display_FA(self:"FA"):
        print("Transition table :")
        lowercase_alphabet = [chr(i) for i in range(ord('a'), ord('z') + 1)] #get alphabets character for links
        table = {str(i): {lowercase_alphabet[j]: [] for j in range(int(self.alphabet_size))} for i in range(self.nb_states)}
        for trans in self.transitions:
            # trans ressemble à "0a1" -> src='0', lettre='a', target='1'
            src, lettre, target = trans[0], trans[1], trans[2:]
            if src in table and lettre in table[src]:
                table[src][lettre].append(target)

        #prints header line
        print("\t","\t","\t",end='')
        for i in range(int(self.alphabet_size)): 
            print("|","\t",lowercase_alphabet[i],"\t",end='')
        print("|")
        print("---------","-" * (16 * (int(self.alphabet_size) + 1)))
        for i in range(self.nb_states):
            state_str = str(i)
            
            prefix = ""
            if state_str in map(str, self.initial_states[1]): 
                prefix += "->"
            if state_str in map(str, self.final_states[1]): 
                prefix += "<-"
            
            
            print(prefix, "\t", "|", "\t", state_str, end='\t') #affiche la 1ere cellulle a gauche avec état et fléche
            
            # Affichage des cellules pour chaque lettre
            
            for j in range(int(self.alphabet_size)):
                lettre = lowercase_alphabet[j]
                targets = table[state_str][lettre]
                
                if not targets:
                    cell_value = "-"
                else:
                    cell_value = ",".join(targets)
                
                print("|", "\t", cell_value, "\t", end='')
            
            print("|") # Fin de ligne

    def is_deterministic(self):
        if self.initial_states[0] != 1:
            return print("The automata is not deterministic because it has more than one initial state.")
        for i in range(int(self.nb_transitions)-1):
            if self.transitions[i][:2] == self.transitions[i+1][:2]:
                return print("The automata is not deterministic because it has more than one transition for the same state and the same letter.")
        return print("The automata is deterministic because it has only one initial state and no more than one transition for the same state and the same letter.")
        
    def is_complete(self):
        for i in range(self.nb_states):
            for j in range(int(self.alphabet_size)):
                if not any(transition.startswith(str(i)+chr(97+j)) for transition in self.transitions):
                    return print("The automata is not complete because it has at least one state that does not have a transition for at least one letter.")
        return print("The automata is complete because all states have a transition for all letters.")


def main():
    selected = "automatons/text_automata.txt"
    FiniteAutomaton = FA.import_FA(selected)
    FiniteAutomaton.print_info()
    FiniteAutomaton.display_FA()
    FiniteAutomaton.is_deterministic()
    FiniteAutomaton.is_complete()

if __name__ == "__main__":
    main()