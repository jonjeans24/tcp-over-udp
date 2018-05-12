# tcp-over-udp

This was a networking assignment that required the student to use UDP to make a file transfer, however, you needed to make it work as it were TCP. 
This program does the following: 
* generates the packets needed to send the file
* generates random errors
* randomly drops packets being sent
* randomly drops ACKs being sent back to the origin
* reconstructs the packets to recreate the original file
