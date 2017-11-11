# receiver.py
# Jonathan Jeans
# 10/07/2017
# Networking
# Assignment 2 - Phase 1


# THIS PROGRAM IS USED WITH THE SENDER.PY PROGRAM. THIS PROGRAM MUST BE RUN FIRST, THEN THE SENDER.PY
# PROGRAM IS RUN FROM A TERMINAL/COMMAND LINE WITH SPECIFIED ARGUMENTS. CHECK SENDER.PY FOR SPECS.

import socket
import pickle
import math

import checksum


def Main():

    host = '127.0.0.1'
    port = 5000
    buffer = 1472

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind((host,port))

    print("Waiting to receive...")

    data, addr = s.recvfrom(buffer)     # RECEIVE FILE NAME AND ADDRESS
    data = data.decode('utf-8')
    print("file name: " + data)
    print("from: " + str(addr))

    file_name = "copy_" + data          # CREATING NEW FILE NAME

    data = "ACK".encode()               # ACKNOWLEDGING CONNECTION
    s.sendto(data, addr)

    data, addr = s.recvfrom(buffer)     # RECEIVE THE FILE SIZE
    file_size = data.decode('utf-8')
    print("File size received: " + file_size)

    num_of_packets = int(file_size) / 1024   # NUMBER OF PACKETS EXPECTED
    num_of_packets = math.ceil(num_of_packets)

    print("Receiving File: " + file_name)

    concat_file_bits = b''                  # USED TO CREATE FILE FROM SENDER
    i = 0
    state = "ACK"

    while True:
        data, addr = s.recvfrom(buffer)
        packet = pickle.loads(data)
        seq = packet[1]
        if checksum.validate_checksum(packet[0],packet[1],packet[2],packet[3]): # IF TRUE "ACK"
            print(str(i) + " RECEIVE: " + packet[0] + ", SEQ: " + str(packet[1]))
            concat_file_bits += packet[2]
            if int(file_size) < 1024:        # ADD SIZE OF DATA TO SEQ NUMBER
                seq += int(file_size)
            else:
                seq += 1024
            packet[0] = state
            packet[1] = seq + 1              # ACK N+1 FOR SEQUENCE NUMBER
            packet[2] = ""
            msg = pickle.dumps(packet)
            s.sendto(msg, addr)
            i += 1
        else:
            # if checksums are not equivalent then the packet is corrupted and last ACK sent to sender
            print("ERROR: Expected packet #" + checksum.generate_checksum(packet[0],packet[1],packet[2]))
            packet[0] = state
            if packet[1] == 0:
                packet[1] = 0
            else:
                packet[1] -= 1024       # SEQ FOR LAST PACKET IF NOT FIRST PACKET
            packet[2] = ""
            print(":::SENDING - " + packet[0] + ", SEQ - " + str(packet[1]))
            msg = pickle.dumps(packet)
            s.sendto(msg, addr)
        if i >= num_of_packets:
            break   # no more packets

    new_file = open(file_name, 'wb')
    new_file.write(concat_file_bits)
    new_file.close()

    print("...File transfer complete")

    s.close()

if __name__ == '__main__':
    Main()