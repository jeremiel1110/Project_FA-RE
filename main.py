import os

from matplotlib import lines

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


    def is_deterministic(self):
        lowercase_alphabet = [chr(i) for i in range(ord('a'), ord('z') + 1)] #get alphabets character for links
        if self.initial_states[0] != 1:
            return print("The automata is not deterministic because it has more than one initial state.")
        for i in range(self.nb_states):
            for j in range(int(self.alphabet_size)):
                if len(self.transitions[str(i)][lowercase_alphabet[j]]) > 1:    
                    print("The automata is not deterministic because it has more than one transition for the same state and the same letter.")
                    return False
        return print("The automata is deterministic because it has only one initial state and no more than one transition for the same state and the same letter.")
    

    def is_complete(self):
        for i in range(self.nb_states):
            for j in range(int(self.alphabet_size)):
                if len(self.transitions[str(i)][chr(j + ord('a'))]) == 0:
                    return print("The automata is not complete because it has at least one state that does not have a transition for at least one letter.")
        return print("The automata is complete because all states have a transition for all letters.")


    def is_standard (self):
        if self.initial_states[0] != 1:
            print("The automata is not standard because it has more than one initial state.")
            return False
        for i in range(self.nb_states):
            for j in range(int(self.alphabet_size)):
                if "0" in self.transitions[str(i)][chr(j + ord('a'))]:
                    print("The automata is not standard because it has a transition to the initial state.")
                    return False
        print("The automata is standard because it has only one initial state and no transition to the initial state.")


    def determinize(self): #we'll create each elt of a FA one by one

        #starting_states
        n_starting_state = ""
        for character in self.initial_states[1]:
            n_starting_state += str(character)+","
        n_starting_state = n_starting_state[:-1] #to remove the last comma

        #transitions
        n_states = {n_starting_state: {chr(i + ord('a')): [] for i in range(int(self.alphabet_size))}}
        n_transitions = {}
        states_to_process = [n_starting_state]

        i=0
        while i<len(states_to_process):                     #iterate until we have processed all the states
            current_state = states_to_process[i]
            for letter in range(int(self.alphabet_size)):   #create the transition possibilities for each letter
                transition = ""
                transition_elements = []
                for states in current_state.split(","):     #split the current state into elements
                    if states != "":                        #to avoid empty states
                        for character in self.transitions[states][chr(letter + ord('a'))]: #transitions for each letters
                            if character not in transition_elements and character != "": #to avoid duplicates and empty states
                                transition_elements.append(character)

                for element in transition_elements:          #format correctly
                    transition += element+","
                transition = transition[:-1] #to remove the last comma
                print("transition :", transition)


                if transition not in n_states.keys() and transition != "":
                    n_states[transition] = {chr(i + ord('a')): [] for i in range(int(self.alphabet_size))}
                    states_to_process.append(transition)

                n_transitions.setdefault(current_state, {})[chr(letter + ord('a'))] = transition

                for trs in n_transitions:
                        print(n_transitions[trs],",",trs)
            i+=1

        n_nb_states = len(n_states)

        #nb_transitions
        n_nb_transitions = len(n_transitions) * int(self.alphabet_size)


        #final states
        n_final_states = (0, [])
        for state in n_states.keys():
            for element in state.split(","):
                print("element :", element," in ", self.final_states[1])
                if element in self.final_states[1]:
                    n_final_states = (n_final_states[0]+1, n_final_states[1] + [state])



        DFA = FA(self.alphabet_size, n_nb_states, (1, [n_starting_state]), n_final_states, n_nb_transitions, n_transitions)

        return DFA
        
def FA_create(selected:str) -> FA:
    with open(selected) as file:
        lines = [line.rstrip() for line in file]

    # TEMP COMMENT
    # for starting states, to make them a tuple like (1, {0}) being (nb of starting states, {list of starting state})
    starting_states_list = []
    for character in lines[2][1:]:
        if character != " ":
            starting_states_list.append(str(character))
    #same for ending
    ending_states_list = []
    for character in lines[3][1:]:
        if character != " ":
            ending_states_list.append(str(character))

    lowercase_alphabet = [chr(i) for i in range(ord('a'), ord('z') + 1)] #get alphabets character for links
    table = {str(i): {lowercase_alphabet[j]: [] for j in range(int(lines[0]))} for i in range(int(lines[1][0]))}
    for trans in lines[5:]:
        src, lettre, target = trans[0], trans[1], trans[2:]
        if src in table and lettre in table[src]:
            table[src][lettre].append(target)

    imported_FA = FA(int(lines[0]), int(lines[1][0]), (int(lines[2][0]), starting_states_list), (int(lines[3][0]), ending_states_list), int(lines[4]), table)

    return imported_FA



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

    #prints header line
    print("\t","\t","\t",end='')
    for i in range(int(FA.alphabet_size)): 
        print("|","\t",lowercase_alphabet[i],"\t",end='')
    print("|")
    print("---------","-" * (16 * (int(FA.alphabet_size) + 1)))
    for i in range(FA.nb_states):
        state_str = str(i)
        
        prefix = ""
        if state_str in map(str, FA.initial_states[1]): 
            prefix += "->"
        if state_str in map(str, FA.final_states[1]): 
            prefix += "<-"
        
        
        print(prefix, "\t", "|", "\t", state_str, end='\t') #affiche la 1ere cellulle a gauche avec état et fléche
        
        # Affichage des cellules pour chaque lettre
        
        for j in range(int(FA.alphabet_size)):

            lettre = lowercase_alphabet[j]
            targets = FA.transitions[state_str][lettre]

            cell_value = ""
            if len(targets) == 0:
                cell_value = "--"
            else:
                for k in range(len(targets)):
                    if targets[k] != ",":
                        cell_value += ""+targets[k]+","
                cell_value = cell_value[:-1] #to remove the last comma

            
            print("|", "\t", cell_value, "\t", end='')
        
        print("|") # Fin de ligne
    


def Ask_for_standardization():
    print("Do you want to standardize it ? (Y/N)")
    while True:
        i=chr(input())
        if i =='Y' or i=='y':
            return True
        if i =='N' or i =='n':
            return False
        else:  
            print("Answer not recognized try again")


def main():
    selected = select_text_automata()
    FA_used = FA_create(selected)
    print_FA(FA_used)

#    FA_used.is_deterministic()
    
#    FA_used.is_complete()

#    if not FA_used.is_standard():
#        if Ask_for_standardization():
#            SFA=standardization(FA_used)

    determinized_FA = FA_used.determinize()
    print_FA(determinized_FA)




main()
