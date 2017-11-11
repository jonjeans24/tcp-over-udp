# message.py
# Jonathan Jeans
# 11/10/2017
# Networking
# Assignment 2 - Phase 2

import random
import pickle

import checksum


class Message:

    # initiate message with an empty list
    def __init__(self):
        self.original_message = []

    # function used to create a packet
    def create_packet(self, state, seq, data):
        packet = [state, seq, data, checksum.generate_checksum(state, seq, data)]
        return packet

    # function used to generate a packet with errors
    def create_error_packet(self, state, seq, data):
        packet = [state, seq, data, checksum.generate_checksum("ERROR", seq, data)]
        return packet

    # function that randomly determines whether a packet is good or corrupted
    def determine_packet(self, state, seq, data, error_percentage):
        rand_num = random.randrange(1, 101)  # GENERATES RANDOM NUMBER BETWEEN 1 AND 100
        if rand_num <= error_percentage:
            packet = Message.create_error_packet(self, state, seq, data)
            print(":::SENT CORRUPTED PACKET:::")
        else:
            packet = Message.create_packet(self, state, seq, data)
        return packet

    # function that creates a list of packets for entire file being sent
    def create_message(self, file_name, num_of_packets, file_size):
        state = "START"                                                     # STATE = START
        seq = 0
        i = 0
        with open(file_name, 'rb') as in_file:
            data = in_file.read(1024)

            while True:
                if data == b'':
                    break                                                   # end of file
                elif i == 0:
                    packet = Message.create_packet(self, state, seq, data)
                elif i != 0 and i < num_of_packets - 1:
                    seq += 1024
                    state = "DATA"                                          # STATE = DATA
                    packet = Message.create_packet(self, state, seq, data)
                else:
                    seq += file_size % 1024
                    state = "END"                                           # STATE = END
                    packet = Message.create_packet(self, state, seq, data)
                    self.original_message.append(pickle.dumps(packet))
                    break
                self.original_message.append(pickle.dumps(packet))
                data = in_file.read(1024)
                i += 1

        in_file.close()