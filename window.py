

class Window:

    def __init__(self, num_of_packets):
        self.window_list = [False] * num_of_packets
        self.window = 5

    
