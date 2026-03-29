from time import time
import os
import sys
import time

from numpy import partition

def select_text_automata():
    automatas = []
    # print("Current Working Directory:", os.getcwd()) # debugging working directory issues
    path='./automatons'
    for file in os.scandir(path):
        if file.name.endswith('.txt'):
           automatas.append(file.name)
    automatas = sorted(automatas, key=lambda x: int(''.join(filter(str.isdigit, x)) or 0))
    selected = 'text_automatas.txt'
    
    print("What FA do you want to read ?")
    # print("selected :",selected)

    for i in range(len(automatas)):
        print(i,".  ",automatas[i],"")

    selected = automatas[int(input())]
    print("FA selected is", selected)
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
            return print("Is it deterministic? The automata is not deterministic because it has more than one initial state.")
        for i in range(self.nb_states):
            for j in range(int(self.alphabet_size)):
                if len(self.transitions[str(i)][lowercase_alphabet[j]]) > 1:    
                    print("Is it deterministic? The automata is not deterministic because it has more than one transition for the same state and the same letter.")
                    return False
        print("Is it deterministic? The automata is deterministic because it has only one initial state and no more than one transition for the same state and the same letter.")
        return True
    

    def is_complete(self):
        for i in range(self.nb_states):
            for j in range(int(self.alphabet_size)):
                if len(self.transitions[str(i)][chr(j + ord('a'))]) == 0:
                    return print("Is it complete? The automata is not complete because it has at least one state that does not have a transition for at least one letter.")
        print("Is it complete? The automata is complete because all states have a transition for all letters.")
        return True


    def is_standard(self):
        if self.initial_states[0] != 1:
            print("The automata is not standard because it has more than one initial state.")
            return False

        initial_state = str(self.initial_states[1][0])

        for state in self.transitions:
            for j in range(int(self.alphabet_size)):
                letter = chr(j + ord('a'))
                targets = self.transitions[state].get(letter, "")

                if targets != "":
                    target_list = [t.strip() for t in targets.split(",") if t.strip() != ""]
                    if initial_state in target_list:
                        print("The automata is not standard because it has a transition to the initial state.")
                        return False

        print("The automata is standard because it has only one initial state and no transition to the initial state.")
        return True

    def epsilon_closure(self, states):
        """
        Returns the epsilon-closure of one state or several states.
        Epsilon transitions use the symbol '*'.
        """

        def parse_targets(targets):
            if targets == "" or targets is None:
                return []

            if isinstance(targets, list):
                return [str(t) for t in targets if str(t) != ""]

            if isinstance(targets, str):
                return [t.strip() for t in targets.split(",") if t.strip() != ""]

            return []

        if isinstance(states, str):
            closure = {states}
            stack = [states]
        else:
            closure = {str(s) for s in states}
            stack = [str(s) for s in states]

        while stack:
            current_state = stack.pop()

            if '*' not in self.transitions[current_state]:
                continue

            epsilon_targets = parse_targets(self.transitions[current_state]['*'])

            for target in epsilon_targets:
                if target not in closure:
                    closure.add(target)
                    stack.append(target)

        return sorted(list(closure))


    def all_epsilon_closures(self):
        closures = {}
        for state in self.transitions.keys():
            closures[state] = self.epsilon_closure(state)
        return closures


    def determinize(self):
        # Helper: convert "", "1", "1,3" into a sorted list without duplicates
        def parse_targets(targets):
            if targets == "" or targets is None:
                return []
            if isinstance(targets, str):
                return sorted(set(t.strip() for t in targets.split(",") if t.strip() != ""))
            if isinstance(targets, list):
                return sorted(set(str(t).strip() for t in targets if str(t).strip() != ""))
            return []

        # Initial DFA state = set of initial NFA states
        initial_set = sorted(set(str(s) for s in self.initial_states[1]))
        initial_name = ",".join(initial_set)

        alphabet = [chr(i + ord('a')) for i in range(int(self.alphabet_size))]

        dfa_transitions = {}
        seen_states = set()
        states_to_process = [initial_name]

        seen_states.add(initial_name)

        while states_to_process:
            current_name = states_to_process.pop(0)
            current_states = [s for s in current_name.split(",") if s != ""]

            dfa_transitions[current_name] = {}

            for letter in alphabet:
                next_states = set()

                for state in current_states:
                    if state in self.transitions:
                        targets = self.transitions[state].get(letter, "")
                        for target in parse_targets(targets):
                            next_states.add(target)

                if len(next_states) == 0:
                    dfa_transitions[current_name][letter] = "P"
                else:
                    next_name = ",".join(sorted(next_states))
                    dfa_transitions[current_name][letter] = next_name

                    if next_name not in seen_states:
                        seen_states.add(next_name)
                        states_to_process.append(next_name)

        # Add sink state P if needed
        need_sink = any(
            dfa_transitions[state][letter] == "P"
            for state in dfa_transitions
            for letter in alphabet
        )

        if need_sink:
            dfa_transitions["P"] = {letter: "P" for letter in alphabet}
            seen_states.add("P")

        # Final states: any DFA state containing at least one NFA final state
        original_finals = set(str(s) for s in self.final_states[1])
        dfa_finals = []

        for state_name in seen_states:
            if state_name == "P":
                continue
            components = state_name.split(",")
            if any(comp in original_finals for comp in components):
                dfa_finals.append(state_name)

        DFA = FA(
            self.alphabet_size,
            len(seen_states),
            (1, [initial_name]),
            (len(dfa_finals), sorted(dfa_finals)),
            len(seen_states) * int(self.alphabet_size),
            dfa_transitions
        )

        return DFA
    
    def completing(self):
        list_of_states = list(self.transitions.keys())
        n_transitions = self.transitions
        for j in range(self.nb_states):
            for letter in range(int(self.alphabet_size)):
                print(list_of_states[j],",",letter)
                if self.transitions[list_of_states[j]][chr(letter + ord('a'))] == "":
                    n_transitions[list_of_states[j]][chr(letter + ord('a'))] = "P"  
        n_transitions["P"] = {chr(i + ord('a')): "P" for i in range(int(self.alphabet_size))} #add the new state P        
        
        CFA = FA(self.alphabet_size, self.nb_states+1, self.initial_states, self.final_states, self.nb_transitions+2, n_transitions)

        return CFA
        
    def standardize(self):
        n_starting_state = "S"
        n_transitions = self.transitions
        n_transitions[n_starting_state] = {chr(i + ord('a')): "" for i in range(int(self.alphabet_size))}
        for letter in range(int(self.alphabet_size)):
            transition = ""
            for initial in self.initial_states[1]:
                for character in n_transitions[str(initial)][chr(letter + ord('a'))]: #transitions for each letters
                    if character != "" and character not in transition: #to avoid empty states
                        transition += str(character)+","
                    print("transition :", transition)
            transition = transition[:-1] #to remove the last comma
            n_transitions[n_starting_state][chr(letter + ord('a'))] = transition    

        SFA = FA(self.alphabet_size, self.nb_states+1, (1, [n_starting_state]), self.final_states, self.nb_transitions, n_transitions)
        
        return SFA
    
    
    def complementary(self):
        final_states_list = {str(state) for state in self.final_states[1]}
        states_list = list(self.transitions.keys())

        complementary_list = []
        for state in states_list:
            if str(state) not in final_states_list:
                complementary_list.append(state)

        complementary_final_states = (len(complementary_list), complementary_list)

        CFA = FA(self.alphabet_size, self.nb_states, self.initial_states, complementary_final_states, self.nb_transitions, self.transitions)
        return CFA
    
    def recognize_word(self, word:str):
        DFA = self.determinize()
        current_state = DFA.initial_states[1][0] #start from the initial state

        for character in word:
            if ord(character) < ord('a') or ord(character) >= ord('a') + int(DFA.alphabet_size):
                print("No")
                return False

            if character not in DFA.transitions[current_state]:
                print("No")
                return False
            next_state = DFA.transitions[current_state][character]

            if next_state == "":
                print("No")
                return False
            current_state = next_state
        
        if current_state in DFA.final_states[1]:
            print("Yes")
            return True
        
        print("No")
        return False

    def minimize(self):
        DFA = self.determinize()

        print("------ MINIMIZATION ------")

        states = list(DFA.transitions.keys())
        alphabet = [chr(i + ord('a')) for i in range(int(DFA.alphabet_size))]
        final_states = set(str(state) for state in DFA.final_states[1])
        non_final_states = set(states) - final_states

        partitions = []
        if len(non_final_states) > 0:
            partitions.append(non_final_states)
        if len(final_states) > 0:
            partitions.append(final_states)

        def print_partitions(parts, step):
            print("Partition", step, ":")
            for i in range(len(parts)):
                print("P" + str(i), "=", sorted(list(parts[i])))

        print_partitions(partitions, 0)

        changed = True
        step = 1

        while changed:
            changed = False
            new_partitions = []

            for group in partitions:
                signatures = {}

                for state in group:
                    signature = []

                    for letter in alphabet:
                        target = DFA.transitions[state][letter]

                        target_group = -1
                        for i in range(len(partitions)):
                            if target in partitions[i]:
                                target_group = i
                                break

                        signature.append(target_group)

                    signature = tuple(signature)

                    if signature not in signatures:
                        signatures[signature] = set()
                    signatures[signature].add(state)

                if len(signatures) > 1:
                    changed = True

                for sig in signatures:
                    new_partitions.append(signatures[sig])

            partitions = new_partitions
            print_partitions(partitions, step)
            step += 1

        if len(partitions) == len(states):
            print("The automaton is already minimal.")
            return DFA

        state_to_group = {}
        for i in range(len(partitions)):
            for state in partitions[i]:
                state_to_group[state] = str(i)

        print("State correspondence table:")
        for i in range(len(partitions)):
            print(str(i), "->", sorted(list(partitions[i])))

        n_transitions = {}
        for i in range(len(partitions)):
            representative = list(partitions[i])[0]
            n_transitions[str(i)] = {}

            print("Transitions for group", i, "based on state", representative, ":")

            for letter in alphabet:
                target = DFA.transitions[representative][letter]
                n_transitions[str(i)][letter] = state_to_group[target]
                print(" ", str(i), "--", letter, "-->", state_to_group[target])

        n_initial_state = state_to_group[DFA.initial_states[1][0]]
        n_final_states_list = []

        for i in range(len(partitions)):
            group_name = str(i)
            for state in partitions[i]:
                if state in final_states:
                    n_final_states_list.append(group_name)
                    break

        MCDFA = FA(
            DFA.alphabet_size,
            len(partitions),
            (1, [n_initial_state]),
            (len(n_final_states_list), n_final_states_list),
            len(partitions) * int(DFA.alphabet_size),
            n_transitions
        )

        return MCDFA
    
    def synchronize(self):
    # transform an asynchronous FA into an equivalent synchronous FA
    # by removing epsilon transitions (*)

        def parse_targets(targets):
            if targets == "" or targets is None:
                return []

            if isinstance(targets, list):
                return [str(t) for t in targets if str(t) != ""]

            if isinstance(targets, str):
                return [t.strip() for t in targets.split(",") if t.strip() != ""]

            return []

        # new transition table without epsilon
        n_transitions = {
            str(i): {chr(j + ord('a')): "" for j in range(int(self.alphabet_size))}
            for i in range(self.nb_states)
        }

        original_final_states = set(str(state) for state in self.final_states[1])

        # final states of the synchronous automaton
        n_final_states_list = []

        for state in range(self.nb_states):
            state = str(state)

            # epsilon-closure of current state
            closure = self.epsilon_closure(state)

            # if one state in the closure is final, then the state becomes final
            for closure_state in closure:
                if closure_state in original_final_states:
                    if state not in n_final_states_list:
                        n_final_states_list.append(state)
                    break

            # build transitions for each real letter
            for letter in range(int(self.alphabet_size)):
                current_letter = chr(letter + ord('a'))
                transition_elements = []

                # first move with the letter from all states in epsilon-closure(state)
                for closure_state in closure:
                    direct_targets = parse_targets(self.transitions[closure_state][current_letter])

                    # then take epsilon-closure of all reached states
                    for target in direct_targets:
                        target_closure = self.epsilon_closure(target)
                        for closure_target in target_closure:
                            if closure_target not in transition_elements:
                                transition_elements.append(closure_target)

                transition_elements = sorted(transition_elements, key=lambda x: int(x))

                transition = ""
                for element in transition_elements:
                    transition += element + ","

                if transition != "":
                    transition = transition[:-1]

                n_transitions[state][current_letter] = transition

        # number of transitions really present in the new automaton
        n_nb_transitions = 0
        for state in n_transitions:
            for letter in n_transitions[state]:
                if n_transitions[state][letter] != "":
                    n_nb_transitions += 1

        Synchronous_FA = FA(
            self.alphabet_size,
            self.nb_states,
            self.initial_states,
            (len(n_final_states_list), n_final_states_list),
            n_nb_transitions,
            n_transitions
        )

        return Synchronous_FA



def FA_create(selected:str) -> FA:
    with open(selected) as file:
        lines = [line.rstrip() for line in file]

    epsilon_here = any(len(trans) >= 2 and trans[1] == '*' for trans in lines[5:] if trans)

    # TEMP COMMENT
    # for starting states, to make them a tuple like (1, {0}) being (nb of starting states, {list of starting state})
    starting_parts = lines[2].split()
    starting_states_list = starting_parts[1:]
    #same for ending
    ending_parts = lines[3].split()
    ending_states_list = ending_parts[1:]

    lowercase_alphabet = [chr(i) for i in range(ord('a'), ord('z') + 1)] #get alphabets character for links
    alpha_keys = {lowercase_alphabet[j]: "" for j in range(int(lines[0]))}
    if epsilon_here:
        alpha_keys['*'] = ""

    table = {str(i): dict(alpha_keys) for i in range(int(lines[1]))}

    for trans in lines[5:]:
        if not trans:
            continue
        letter_idx = next((i for i, c in enumerate(trans) if not c.isdigit()), None)
        if letter_idx is None:
            continue
        src = trans[:letter_idx]
        lettre = trans[letter_idx]
        target = trans[letter_idx + 1:]
        if src in table and lettre in table[src]:
            if table[src][lettre] == "":
                table[src][lettre] = target
            else:
                table[src][lettre] += "," + target

    imported_FA = FA(int(lines[0]), int(lines[1]), (int(starting_parts[0]), starting_states_list), (int(ending_parts[0]), ending_states_list), int(lines[4]), table)

    return imported_FA, epsilon_here



def print_FA(FA:FA):
    print("Alphabet size :", FA.alphabet_size)
    print("Number of states :", FA.nb_states)
    print("Initial states :", FA.initial_states)
    print("Final states :", FA.final_states)
    print("Number of transitions :", FA.nb_transitions)
    print("Transition table :")
    print_FA_table(FA)
    
    

def print_FA_table(FA:FA):
    lowercase_alphabet = [chr(i) for i in range(ord('a'), ord('z') + 1)]
    has_epsilon = any('*' in FA.transitions[s] for s in FA.transitions)
    state_names = list(FA.transitions.keys())

    letters_to_print = [lowercase_alphabet[j] for j in range(int(FA.alphabet_size))]
    if has_epsilon:
        letters_to_print.append('*')

    # Compute column width to fit the longest state name or cell value
    all_vals = list(state_names)
    for state_str in state_names:
        for lettre in letters_to_print:
            t = FA.transitions[state_str].get(lettre, "")
            all_vals.append(t if t else "--")
    col_w = max(6, max(len(str(v)) for v in all_vals) + 2)
    prefix_w = 4  # max is "-><-"

    # Header
    print(f"{'':>{prefix_w}} | {'':^{col_w}}", end='')
    for l in letters_to_print:
        print(f" | {l:^{col_w}}", end='')
    print(" |")
    sep_len = prefix_w + 3 + col_w + (col_w + 3) * len(letters_to_print) + 2
    print("-" * sep_len)

    for state_str in state_names:
        prefix = ""
        for initial in FA.initial_states[1]:
            if str(initial) == state_str:
                prefix += "->"
                break
        for final in FA.final_states[1]:
            if str(final) == state_str:
                prefix += "<-"
                break
        if "<-" not in prefix:
            for element in state_str.split(","):
                for final in FA.final_states[1]:
                    if str(final) == element:
                        prefix += "<-"
                        break
                if "<-" in prefix:
                    break

        print(f"{prefix:>{prefix_w}} | {state_str:^{col_w}}", end='')

        for lettre in letters_to_print:
            targets = FA.transitions[state_str].get(lettre, "")
            cell_value = ""
            if targets == "" or targets is None:
                cell_value = "--"
            elif isinstance(targets, str):
                cell_value = targets
            elif len(targets) == 0:
                cell_value = "--"
            else:
                for k in range(len(targets)):
                    if targets[k] != ",":
                        cell_value += ""+targets[k]+","
                cell_value = cell_value[:-1]

            print(f" | {cell_value:^{col_w}}", end='')

        print(" |")




def main():
    debug=False
    if len(sys.argv) > 1 and sys.argv[1]=="--debug":
        debug=True
    if not debug:
        """
        selected = select_text_automata()
        FA_used,asyncronous = FA_create(selected) #we get the automata and if it is asyncronous or not
        print_FA(FA_used)
        if asyncronous: #if it's asyncronous we do something (epsuilon closure) so that the rest can run without any issue
            print("This automaton contains epsilon transitions.")
            print("Epsilon-closure of each state:")
            closures = FA_used.all_epsilon_closures()
            for state in closures:
                print("E(", state, ") =", closures[state])
        else:
            pass
    #    FA_used.is_deterministic()
        
    #    FA_used.is_complete()

        
        if FA_used.is_standard == False :
            print("Do you want to standardize it ?")
            if chr(input())=='Y'|'y'|'yes'|'YES'|'Yes':
                Standardized_FA=FA_used.standardize


        determinized_FA = FA_used.determinize()
        print_FA(determinized_FA)

        standardized_FA = FA_used.standardize()
        print_FA(standardized_FA)
        
        CFA = FA_used.complementary()
        print_FA(CFA)
        """


        def loop():
            keepGoing = True

            while keepGoing:


                # print("What FA do you want to read ?")
                selected = select_text_automata()
                print("")
                FA_selected, asyncronous = FA_create(selected)
                
                print_FA_table(FA_selected)
                print("")

                if asyncronous: #if it's asyncronous we do something (epsuilon closure) so that the rest can run without any issue
                    print("This automaton contains epsilon transitions.")
                    print("Epsilon-closure of each state:")
                    closures = FA_selected.all_epsilon_closures()
                    for state in closures:
                        print("E(", state, ") =", closures[state])
                    print("")

                    print("Here is the equivalent synchronous automaton:")
                    FA_selected = FA_selected.synchronize()
                    print_FA_table(FA_selected)
                    print("")

                    asyncronous = False
                else:
                    pass
    
                deterministic = FA_selected.is_deterministic()
                print("")

                complete = FA_selected.is_complete()
                print("")

                if not deterministic or not complete:
                    print("Do you want to obtain an equivalent complete deterministic FA ? (y, Y, yes, Yes, YES)")
                    if str(input()) in ["Y", "y", "yes", "YES", "Yes"]:
                        if not deterministic:
                            FA_selected = FA_selected.determinize()
                        elif not complete:
                            FA_selected = FA_selected.completing()

                    print_FA_table(FA_selected)
                    print("")

                standard = FA_selected.is_standard()
                print("")

                if not standard:
                    print("Do you want to standardize it ? (y, Y, yes, Yes, YES)")
                    if str(input()) in ["Y", "y", "yes", "YES", "Yes"]:
                        FA_selected = FA_selected.standardize()
                        print_FA_table(FA_selected)
                        print("")

                print("Here is the equivalent minimal automaton")
                FA_selected = FA_selected.minimize()
                print_FA_table(FA_selected)
                print("")

                print("Do you want to construct an automaton recognizing the complementary language ? (y, Y, yes, Yes, YES)")
                if str(input()) in ["Y", "y", "yes", "YES", "Yes"]:
                    FA_selected = FA_selected.complementary()
                    print_FA_table(FA_selected)
                print("")

                print("Do you want to do the word recognition test ? (y, Y, yes, Yes, YES)")
                if str(input()) in ["Y", "y", "yes", "YES", "Yes"]:
                    print("Enter a word to test it (type \"end\" to stop the test):")
                    word = input()
                    while word != "end":
                        FA_selected.recognize_word(word)
                        word = input()
                print("")
                

                print("Do you want to choose a new automaton ? (y, Y, yes, Yes, YES)")
                if str(input()) in ["Y", "y", "yes", "YES", "Yes"]:
                    keepGoing = True
                else:
                    keepGoing = False
                print("")

        loop()


    if debug :
        with open("debug_ouput_"+str(time.ctime())+".debug",'w') as f:
            sys.stdout=f
            path='./automatons'
            available_list=[]
            for file in os.scandir(path):
                if file.name.endswith('.txt'):
                    available_list.append(file.name)
            available_list = sorted(available_list, key=lambda x: int(''.join(filter(str.isdigit, x)) or 0))
            for i in range(0,len(available_list)):
                current = path+'/'+available_list[i]
                print("----------------CURRENT AUTOMATA : ",current,"----------------")
                FA_used=FA_create(current)
                print_FA(FA_used)
                FA_used.is_deterministic()
                FA_used.is_complete() 
                FA_used.is_standard()
                FA_Standardize=FA_used.standardize()
                print("----------------STANDARDIZED AUTOMATA----------------")
                print_FA(FA_Standardize)
                FA_Complete=FA_used.completing()
                print("----------------COMPLETED AUTOMATA----------------")
                print_FA(FA_Complete)
                if FA_used.is_complete() and FA_used.is_standard() == False :
                    FA_determinized=FA_used.determinize()
                    print("----------------DETERMINIZED AUTOMATA----------------")
                    print_FA(FA_determinized)
                #FA_completementary=FA_determinized.complementary()
                print("----------------COMPLEMENTARY AUTOMATA----------------")
                #print(FA_completementary)
                #FA_completmentary.recognize_word
                print("-----------------------------------------\t\t NEXT AUTOMATA\t\t-----------------------------------------")

main()

            






