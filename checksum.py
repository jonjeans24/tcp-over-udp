# checksum.py
# Jonathan Jeans
# 10/07/2017
# Networking
# Assignment 2 - Phase 1

import binascii


# Used to validate checksum after packet sent to receiver
def validate_checksum(state, seq, data, checksum):
    compare_checksum = generate_checksum(state, seq, data)
    if compare_checksum == checksum:
        return True
    else:
        return False


# takes entire message from packet and generates checksum
def generate_checksum(state, seq, data):
    message = state.encode('utf-8') + str(seq).encode('utf-8') + data
    return str(binascii.crc32(message) & 0xffffffff)
