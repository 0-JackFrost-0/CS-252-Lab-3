import numpy as np


def hamming_code(data):
    p0 = p1 = p2 = p4 = p8 = 0
    net_parity = 0
    hamming_code = [p0, p1, p2] + [data[0]] + \
        [p4] + data[1:4] + [p8] + data[4:]
    for i, bit in enumerate(hamming_code):
        if bit == 1:
            net_parity ^= i
    len_net_parity = len(bin(net_parity)[2:])
    net_parity = bin(net_parity)[2:]
    if len_net_parity < 4:
        for i in range(4 - len_net_parity):
            net_parity = '0' + net_parity
    for i, bit in enumerate(net_parity):
        if i == 0:
            p8 = int(bit)
        elif i == 1:
            p4 = int(bit)
        elif i == 2:
            p2 = int(bit)
        elif i == 3:
            p1 = int(bit)
    for i in range(len(hamming_code)):
        p0 ^= hamming_code[i]
    hamming_code = [p0, p1, p2] + [data[0]] + \
        [p4] + data[1:4] + [p8] + data[4:]
    return hamming_code


def correct_error(hamming_code):
    net_parity = 0
    enumerated = enumerate(hamming_code)
    for i, bits in enumerated:
        if bits == 1:
            net_parity ^= i
    if net_parity != 0:
        hamming_code[net_parity] = 1 - hamming_code[net_parity]
    return hamming_code


def corrected_data(corrected_hamming_code):
    corrected_data = [corrected_hamming_code[3], corrected_hamming_code[5]
                      ] + corrected_hamming_code[6:8] + corrected_hamming_code[9:]
    return corrected_data
