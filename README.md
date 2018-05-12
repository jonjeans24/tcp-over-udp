# tcp-over-udp

This was a networking assignment that required the student to use UDP to make a file transfer, however, you needed to make it work as it were TCP. 

This program does the following: 
* generates the packets needed to send the file
* generates random errors
* randomly drops packets being sent
* randomly drops ACKs being sent back to the origin
* uses a window of size 5 to send packets; window moves as ACKs are received for packets
* reconstructs the packets to recreate the original file

RUN SENDER.PY AFTER THE RECEIVER.PY PROGRAM HAS BEEN STARTED. THIS PROGRAM MUST BE RUN FROM THE
COMMAND LINE/TERMINAL WITH THE FOLLOWING SYNTAX:
* python3 sender.py <file> <host> <port> <error>
* file = file you will be sending from current directory to receiver directory
* host = host that is connecting to receiver host
* port = port for sender. Receiver port is hard coded to 5000 for this phase.
* error = integer from 0-99. This value will generate corrupt packets in relation to the number entered. 0 = 0%, 50 = 50%, etc.
