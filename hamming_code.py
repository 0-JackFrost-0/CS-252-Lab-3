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


def hamming_to_conveyable(hamming_code):
    return hamming_code + [0, 0]


def conveyable_to_hamming(conveyable_code):
    return conveyable_code[:17]


def get_input():
    bits = input("Type in Binary String to Send: ")
    bit_to_change = int(input("Type in the bit position to change: "))
    if len(bits) % 11 != 0:
        bits += '0' * (11 - len(bits) % 11)
    padded_bits = 11 - len(bits) % 11
    bits = [int(bit) for bit in bits]
    hamming_packets = []
    for i in range(len(bits)//11):
        hamming_packets.append(hamming_code(bits[i*11:]))
    conveyable_packets = []
    for packet in hamming_packets:
        conveyable_packets.append(hamming_to_conveyable(packet))
    packet_to_change = bit_to_change//11
    hamming = conveyable_packets[packet_to_change].copy()
    if bit_to_change >= len(bits):
        print("Invalid bit position")
    elif bit_to_change == 0:
        print("Bruh, you can't change the parity bit")
        hamming[3] = 1 - hamming[3]
    elif bit_to_change > 0 and bit_to_change < 4:
        hamming[4 + bit_to_change] = 1 - \
            hamming[4 + bit_to_change]
    elif bit_to_change > 3:
        hamming[5 + bit_to_change] = 1 - \
            hamming[5 + bit_to_change]
    correct_conveyable_packets = conveyable_packets.copy()
    conveyable_packets[packet_to_change] = hamming
    return correct_conveyable_packets, conveyable_packets


correct_hamming_codes, changed_hamming_codes = get_input()
print(correct_hamming_codes)
print(changed_hamming_codes)
