# window.py
# Jonathan Jeans
# 11/10/2017
# Networking
# Assignment 2 - Phase 2


class Window:

    # function initiates a new Window object with a list of booleans and a window size of 5
    def __init__(self, num_of_packets):
        self.window_list = [False] * num_of_packets
        self.window = 5

    # This function moves the current window to the next slot that is False.
    # If current position matches the size of the list then the index - 5 is returned.
    # Need this so that user doesnt point to location out of list.
    def move_window(self, curr_pos):
        if curr_pos == len(self.window_list) - 5:
            return curr_pos
        else:
            for x in range(0, self.window + 1):
                if not self.window_list[curr_pos + x]:
                    return curr_pos + x
            return curr_pos + x

    # Function used to check if all ACKs were attained
    # Need this to exit While-loop in sender.py file
    def check_for_false(self):
        for x in self.window_list:
            if x is False:
                return False
        return True
