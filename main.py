import os

def select_text_automata():
    automatas = []
    path='./automatons'
    for file in os.scandir(path):
        if file.name.endswith('.txt'):
            automatas.append(file.name)
    selected = 'text_automatas.txt'
    
    print("What automata do you want to choose ?")
    print("selected :",selected)

    for i in range(len(automatas)):
        print(i,".  ",automatas[i],"")

    selected = automatas[int(input())]
    return path+'/'+selected

############### DO NOT MODIFY ABOVE THIS LINE ###############

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


    def is_deterministic(self):
        if self.initial_states[0] != 1:
            return print("The automata is not deterministic because it has more than one initial state.")
        for i in range(int(self.nb_transitions)-1):
            if self.transitions[i][:1] == self.transitions[i+1][:1]:
                return print("The automata is not deterministic because it has more than one transition for the same state and the same letter.")
            else:
                return print("true")
        return print("The automata is deterministic because it has only one initial state and no more than one transition for the same state and the same letter.")
    
    def is_complete(self):
        for i in range(self.nb_states[0]):
            for j in range(int(self.alphabet_size)):
                if not any(transition.startswith(str(i)+chr(97+j)) for transition in self.transitions):
                    return print("The automata is not complete because it has at least one state that does not have a transition for at least one letter.")
        return print("The automata is complete because all states have a transition for all letters.")
            



def FA_create(selected:str) -> FA:
    with open(selected) as file:
        lines = [line.rstrip() for line in file]

    # TEMP COMMENT
    # for starting states, to make them a tuple like (1, {0}) being (nb of starting states, {list of starting state})
    starting_states_list = []
    for character in lines[1][1:]:
        if character != " ":
            starting_states_list.append(int(character))
    #same for ending
    ending_states_list = []
    for character in lines[2][1:]:
        if character != " ":
            ending_states_list.append(int(character))

    FA1 = FA(lines[0], (int(lines[1][0]), starting_states_list), (int(lines[2][0]), ending_states_list), lines[3], lines[4], lines[5:])

    return FA1




def print_FA(FA:FA):
    print("Alphabet size :", FA.alphabet_size)
    print("Number of states :", FA.nb_states)
    print("Initial states :", FA.initial_states)
    print("Final states :", FA.final_states)
    print("Number of transitions :", FA.nb_transitions)
    print("Transition table :")
    print_FA_table(FA)
    
    
def print_FA_table(FA:FA):
    lowercase_alphabet = [chr(i) for i in range(ord('a'), ord('z') + 1)] #get alphabets character for links
    table = {str(i): {lowercase_alphabet[j]: [] for j in range(int(FA.alphabet_size))} for i in range(int(FA.nb_states[0]))}
    for trans in FA.transitions:
        # trans ressemble à "0a1" -> src='0', lettre='a', target='1'
        src, lettre, target = trans[0], trans[1], trans[2:]
        if src in table and lettre in table[src]:
            table[src][lettre].append(target)

    #prints header line
    print("\t","\t","\t",end='')
    for i in range(int(FA.alphabet_size)): 
        print("|","\t",lowercase_alphabet[i],"\t",end='')
    print("|")
    print("---------","-" * (16 * (int(FA.alphabet_size) + 1)))
    for i in range(int(FA.nb_states[0])):
        state_str = str(i)
        
        prefix = ""
        if state_str in map(str, FA.initial_states): 
            prefix += "->"
        if state_str in map(str, FA.final_states): 
            prefix += "<-"
        
        
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
    


def Ask_for_standardization():
    print("Do you want to standardize it ? (Y/N)")
    while True:
        i=char(input())
        if i =='Y' or i=='y':
            return True
        if i =='N' or i =='n':
            return False
        else:  print("Answer not recognized try again")

def main():
    selected = select_text_automata()
    FA_used = FA_create(selected)
    FA_used.Display_FA()
    print_FA(FA_used)

    FA_used.is_deterministic()
    
    FA_used.is_complete()


main()
