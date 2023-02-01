import numpy as np
from math import ceil

# adds parity bits to the message
def hamming_code(data):
    p0 = p1 = p2 = p4 = p8 = 0
    net_parity = 0
    hamming_code = [p0, p1, p2] + [data[0]] + [p4] + data[1:4] + [p8] + data[4:]
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
    hamming_code = [p0, p1, p2] + [data[0]] + [p4] + data[1:4] + [p8] + data[4:]
    return hamming_code

# corrects the error in the found in the code
def correct_error(hamming_code):
    net_parity = 0
    enumerated = enumerate(hamming_code)
    for i, bits in enumerated:
        if bits == 1:
            net_parity ^= i
    if net_parity != 0:
        hamming_code[net_parity] = 1 - hamming_code[net_parity]
    return hamming_code

# removes parity bits
def corrected_data(corrected_hamming_code):
    corrected_data = [corrected_hamming_code[3], corrected_hamming_code[5]
                      ] + corrected_hamming_code[6:8] + corrected_hamming_code[9:]
    return corrected_data

# converts 16 bit hamming code to 21 bit code to send over the channel
def hamming_to_conveyable(hamming_code, num_padded_bits):
    binary_num = bin(num_padded_bits).replace("0b", "").zfill(5)
    conveyable = hamming_code + [int(bit) for bit in binary_num] 
    return conveyable

# removes the 5 extra bits added to the hamming code, and returns the chopped message, with the number of padded bits
def conveyable_to_hamming(conveyable_code):
    return conveyable_code[:16]


def get_input():
    bits = input("Type in Binary String to Send: ")
    bit_to_change = int(input("Type in the bit position to change: "))
    padded_bits = 11 - len(bits) % 11 if len(bits) % 11 != 0 else 0
    num_packets = ceil(len(bits)/11)
    
    if len(bits) % 11 != 0:
        bits += '0' * padded_bits

    # performs hamming code on the message
    bits = [int(bit) for bit in bits]
    hamming_packets = []
    for i in range(num_packets):
        hamming_packets.append(hamming_code(bits[i*11:(i+1)*11]))
        
    # changes the bit in the message
    packet_to_change = bit_to_change//11
    bit_to_change = bit_to_change % 11
    hamming = hamming_packets[packet_to_change].copy()
    if bit_to_change >= (len(bits)-padded_bits):
        print("Invalid bit position")
    elif bit_to_change == 0:
        hamming[3] = 1 - hamming[3]
    elif bit_to_change > 0 and bit_to_change < 4:
        hamming[4 + bit_to_change] = 1 - hamming[4 + bit_to_change]
    elif bit_to_change > 3:
        hamming[5 + bit_to_change] = 1 - hamming[5 + bit_to_change]
    hamming_packets[packet_to_change] = hamming
    
    conveyable_packets = []
    # makes message conveyable
    packet_no = 0
    for packet in hamming_packets:
        packet_no += 1
        if packet_no == num_packets:
            conveyable_packets.append(hamming_to_conveyable(packet, padded_bits))
        else:
            conveyable_packets.append(hamming_to_conveyable(packet, 0))

    # correct_conveyable_packets = conveyable_packets.copy()
    # conveyable_packets[packet_to_change] = hamming
    # return correct_conveyable_packets, conveyable_packets
    return conveyable_packets

def get_output(conveyable_packets):
    hamming_packets = []
    num_packets = 0
    for packet in conveyable_packets:
        num_packets += 1
        hamming_packets.append(conveyable_to_hamming(packet))
        if num_packets == len(conveyable_packets):
            num_of_padding = int(''.join(map(str, packet[16:])), 2)
    corrected_hamming_packets = []
    for packet in hamming_packets:
        corrected_hamming_packets.append(correct_error(packet))
    corrected_packets = []
    num_packets = 0
    for packet in corrected_hamming_packets:
        num_packets += 1
        if num_packets == len(corrected_hamming_packets):
            # print(num_of_padding)
            if num_of_padding != 0:
                corrected_packets.append(corrected_data(packet)[:-num_of_padding])
            else:
                corrected_packets.append(corrected_data(packet))
        else:
            corrected_packets.append(corrected_data(packet))
    bits = ''
    # print(corrected_hamming_packets)
    for packet in corrected_packets:
        for bit in packet:
            bits += str(bit)
    return bits

# correct_hamming_codes, changed_hamming_codes = get_input()
# print(get_output(get_input()))
# print(changed_hamming_codes)
# print(corrected_data(conveyable_to_hamming(correct_hamming_codes[0])))
# print(corrected_data(conveyable_to_hamming(changed_hamming_codes[0])))
# print(corrected_data(correct_error(conveyable_to_hamming(changed_hamming_codes[0]))))
# ham  = get_input()
# print(ham)
# print(get_output(ham))