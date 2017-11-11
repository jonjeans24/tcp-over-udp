# sender.py
# Jonathan Jeans
# 10/07/2017
# Networking
# Assignment 2 - Phase 1

# THIS PROGRAM IS RUN AFTER THE RECEIVER.PY PROGRAM HAS BEEN STARTED. THIS PROGRAM MUST BE RUN FROM THE
# COMMAND LINE/TERMINAL WITH THE FOLLOWING SYNTAX:
#                   python3 sender.py <file> <host> <port> <error>
#                   file = file you will be sending from current directory to receiver directory
#                   host = host that is connecting to receiver host
#                   port = port for sender. Receiver port is hard coded to 5000 for this phase.
#                   error = integer from 0-99. This value will generate corrupt packets in relation to the number
#                           entered. 0 = 0%, 50 = 50%, etc.

import socket
import pickle
import os
import sys
import math

import message


# ERROR CHECKING FOR THE ARGUMENTS ENTERED BY THE USER
def check_for_error(file_name, port, error):
    check_format = "Check Format: sender.py <file> <host> <port> <error>"
    if os.path.exists(file_name):
        print("File Exists: SUCCESS")
    else:
        print("File Exists: FAILURE")
        print(check_format)
        sys.exit()
    if port == 5000:            # port 5000 currently reserved for the receiver
        print("Port Available: FAILURE")
        print("Port 5000 is reserved for the receiver")
        print(check_format)
        sys.exit()
    else:
        print("Port Available: SUCCESS")
    if error > 99 or error < 0:
        print("Valid Error: FAILURE")
        print("Error must be between 0 and 99")
        print(check_format)
        sys.exit()
    else:
        print("Valid Error: SUCCESS")


def Main():
    # Error checking to verify fields are integer values
    try:
        port = 5001#int(sys.argv[3]) #TODO uncomment when program is ready
        error = 15 #int(sys.argv[4])
    except:
        print("Error: An invalid integer was entered")
        print("Check your <port> and <error> values.")
        sys.exit()

    host = '127.0.0.1' #sys.argv[2]
    file_name = 'baby.jpg' #sys.argv[1]
    buffer = 1472

    check_for_error(file_name, port, error)

    # this is the receiver connection
    # needed for transfers back and forth
    server = ('127.0.0.1', 5000)        # Currently have this hard coded but can change for phase 2
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.bind((host, port))
    except:
        print("An invalid host was entered.")
        print("Check Format: sender.py <file> <host> <port> <error>")
        sys.exit()


    print("Sender Started...")

    s.sendto(file_name.encode('utf-8'), server)     # ESTABLISHING A CONNECTION
    print("Connecting to receiver...")

    try:
        data, addr = s.recvfrom(buffer)
    except:
        print("A connection was either lost or never created.")
        print("Make sure receiver.py is running.")
        sys.exit()

    data = data.decode('utf-8')
    print("From receiver: " + data)

    if data == "ACK":                               # LOOKING FOR RETURNED ACK

        file_size = os.path.getsize(file_name)      # GET THE SIZE OF FILE
        print("Sending file size: " + str(file_size))

        num_of_packets = int(file_size) / 1024      # NUMBER OF PACKETS SENDING
        num_of_packets = math.ceil(num_of_packets)

        print("NUM OF PACKETS: " + str(num_of_packets))

        s.sendto(str(file_size).encode('utf-8'), addr)

        print("File sending...")                    # BEGINNING FILE TRANSFER

        original_file = message.Message()           # CREATES MESSAGE FROM ORIGINAL FILE
        original_file.create_message(file_name, num_of_packets, file_size)

        i = 0
        seq = 0
        while True:
            if i == num_of_packets:
                break

            # either sends correct packet or corrupt packet
            curr_packet = original_file.original_message[i]
            curr_packet = pickle.loads(curr_packet)
            curr_state = curr_packet[0]
            curr_seq = curr_packet[1]
            curr_data = curr_packet[2]

            curr_packet = original_file.determine_packet(curr_state, curr_seq, curr_data, error)

            msg = pickle.dumps(curr_packet)
            s.sendto(msg, addr)

            ack, addr = s.recvfrom(buffer)  # RECEIVE ACK FROM RECEIVER
            packet = pickle.loads(ack)
            print(str(i) + " RECEIVE: " + packet[0] + ", SEQ: " + str(packet[1]))
            if packet[1] == seq + 1024 + 1 or packet[1] == seq + file_size + 1:
                i += 1
                seq += 1024
            elif packet[1] >= file_size:
                break
            else:
                if seq == 0:
                    seq = 0

        print("...File Transfer complete")

    s.close()

if __name__ == '__main__':
    Main()
