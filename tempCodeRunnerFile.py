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