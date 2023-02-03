import sounddevice as sd
from scipy.fftpack import fft
import numpy as np
import time
from hamming_code import *
import threading

# Function to play a note for a given duration
def play_note(frequency, duration):
    samples = np.arange(44100 * duration)
    note = np.sin(2 * np.pi * frequency * samples / 44100)
    sd.play(note, blocking=True)
    print("Playing note: ", frequency)

note_map = {
    "000": "Sa",
    "001": "Re1",
    "011": "Ga3",
    "010": "Ma1",
    "110": "Pa",
    "111": "Dha1",
    "101": "Ni3",
    "100": "SaU",
}

# Mayamaalava Gowla Melakarta Raagam
def bits_to_notes(bits):
    return [note_map[bits[i : i + 3]] for i in range(0, len(bits), 3)]

map_note = {}
for key,value in note_map.items():
    map_note[value] = key

# Define the Carnatic notes and their frequencies
sa_frequency = 280*10  # Sa frequency in Hz
carnatic_notes = {
    "Sa": sa_frequency,
    "Re1": sa_frequency * 256 / 243,
    "Re2": sa_frequency * 9 / 8,
    "Ga2": sa_frequency * 32 / 27,
    "Ga3": sa_frequency * 81 / 64,
    "Ma1": sa_frequency * 4 / 3,
    "Ma2": sa_frequency * 729 / 512,
    "Pa": sa_frequency * 3 / 2,
    "Dha1": sa_frequency * 128 / 81,
    "Dha2": sa_frequency * 27 / 16,
    "Ni2": sa_frequency * 16 / 9,
    "Ni3": sa_frequency * 243 / 128,
    "SaU": sa_frequency * 2,
    "Re1U": sa_frequency*2 * 256 / 243
}

def receive():
    Job = input("Would you like to TRANSMIT, RECEIVE or END?  ")

    if Job == "TRANSMIT":
        
        packets = get_input()
        packet_ = []
        for packet in packets:
            packet = map(str,packet)
            packet = "".join(packet)
            packet_.append(packet)
        while True:
            if time.time()%3 == 0:
                for packet in packet_:
                    bits = packet
                    message_to_send = bits_to_notes(bits)
                    print(message_to_send)

                    # Play the aarohanam of the Mohanam raga
                    for note in message_to_send:
                        play_note(carnatic_notes[note], 2)
                play_note(carnatic_notes["Re1U"],2)
                break
    elif Job == "RECEIVE":
        while True:
            if time.time()%3 == 0:
                Done = False
                rec_freq = []
                received_data = []
                count_nothing=0
                while not Done:
                    fs = 44100
                    duration = 2
                    data = sd.rec(int(fs * duration), fs, channels=1)
                    sd.wait()  # wait for recording to finish
                    # take the FFT of the recorded audio
                    fft_out = fft(data[:, 0])

                    # find the index of the maximum value in the spectrum
                    max_index = np.argmax(np.abs(fft_out))

                    # calculate the frequency of the maximum value
                    frequency = max_index * fs / len(data)
                    print("Receiving:", end=" ")
                    if (frequency > carnatic_notes["Sa"] - 37.5) and (
                        carnatic_notes["Sa"] + 37.5 > frequency
                    ):
                        count_nothing = 0
                        print("Sa")
                        received_data.append(map_note['Sa'])
                    elif (frequency > carnatic_notes["Ma1"] - 37.5) and (
                        carnatic_notes["Ma1"] + 37.5 > frequency
                    ):
                        count_nothing = 0
                        print('Ma1')
                        received_data.append(map_note['Ma1'])
                    elif (frequency > carnatic_notes["Re1"] - 37.5) and (
                        carnatic_notes["Re1"] + 37.5 > frequency
                    ):
                        count_nothing = 0
                        print('Re1')
                        received_data.append(map_note['Re1'])
                    elif (frequency > carnatic_notes["Ga3"] - 37.5) and (
                        carnatic_notes["Ga3"] + 37.5 > frequency
                    ):
                        count_nothing = 0
                        print(carnatic_notes['Ga3'])
                        received_data.append(map_note['Ga3'])
                    elif (frequency > carnatic_notes["Pa"] - 37.5) and (
                        carnatic_notes["Pa"] + 37.5 > frequency
                    ):
                        count_nothing = 0
                        print("Pa")
                        received_data.append(map_note['Pa'])
                    elif (frequency > carnatic_notes["Dha1"] - 37.5) and (
                        carnatic_notes["Dha1"] + 37.5 > frequency
                    ):
                        count_nothing = 0
                        print("Dha1")
                        received_data.append(map_note['Dha1'])
                    elif (frequency > carnatic_notes["Ni3"] - 37.5) and (
                        carnatic_notes["Ni3"] + 37.5 > frequency
                    ):
                        count_nothing = 0
                        print("Ni3")
                        received_data.append(map_note['Ni3'])
                    elif (frequency > carnatic_notes["SaU"] - 37.5) and (
                        carnatic_notes["SaU"] + 37.5 > frequency
                    ):
                        count_nothing = 0
                        print("SaU")
                        received_data.append(map_note['SaU'])
                    elif (frequency > carnatic_notes["Re1U"] - 37.5) and (
                        carnatic_notes["Re1U"] + 37.5 > frequency):
                        break
                    else:
                        count_nothing+=1
                        print("Nothing")

                    rec_freq.append(frequency)

                    if count_nothing > 5:
                        break

                    # Done = True
                    # if len(rec_freq) < 20:
                    #     Done = False

                    # else:
                    #     for a in rec_freq:
                    #         if a > 200:
                    #             Done = False
                    #     rec_freq.pop(0)
                print(received_data)
                rec_data = ''
                for strn in received_data:
                    rec_data = rec_data + strn
                print(rec_data)
                packets = [rec_data[21*i:21*i+21] for i in range(len(rec_data)//21)]
                packets_ = []
                for i in range(len(packets)):
                    packets_.append([int(char) for char in packets[i]])
                print(packets)
                print(packets_)
                out = get_output(packets_)
                print(f"Message received is: {out}")
                break

def sleep():
    time.sleep(3)

while True:
    t1 = threading.Thread(target=receive)
    t2 = threading.Thread(target = sleep)

    t2.start()
    t1.start()

    t1.join()
    t2.join()

    break