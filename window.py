# window.py
# Jonathan Jeans
# 11/10/2017
# Networking
# Assignment 2 - Phase 2


class Window:

    def __init__(self, num_of_packets):
        self.window_list = [False] * num_of_packets
        self.window = 5

    def move_window(self, curr_pos):
        if curr_pos == len(self.window_list) - 5:
            return curr_pos
        else:
            for x in range(0, self.window + 1):
                if not self.window_list[curr_pos + x]:
                    return curr_pos + x
            return curr_pos + x

    # function used to check if all ACKs were attained
    def check_for_false(self):
        for x in self.window_list:
            if x is False:
                return False
        return True
