import sounddevice as sd
from scipy.fftpack import fft
import numpy as np
import time
import threading

# Mayamaalava Gowla Melakarta Raagam
def bits_to_notes(bits):
    note_map = {
        "000": "Sa",
        "001": "Re1",
        "010": "Ga3",
        "011": "Ma1",
        "100": "Pa",
        "101": "Dha1",
        "110": "Ni3",
        "111": "SaU",
    }
    return [note_map[bits[i : i + 3]] for i in range(0, len(bits), 3)]


# Define the Carnatic notes and their frequencies
sa_frequency = 280*5  # Sa frequency in Hz
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
}


# while True:
#     Job = input("Would you like to TRANSMIT, RECEIVE or END?  ")

#     if Job == "TRANSMIT":

#         bits = input("Type in Binary String to Send: ")
#         if len(bits) % 3 == 1:
#             bits = bits + "00"
#         elif len(bits) % 3 == 2:
#             bits = bits + "0"

#         print(bits)
#         message_to_send = bits_to_notes(bits)
#         print(message_to_send)

#         # Function to play a note for a given duration
#         def play_note(frequency, duration):
#             samples = np.arange(44100 * duration)
#             note = np.sin(2 * np.pi * frequency * samples / 44100)
#             sd.play(note, blocking=True)
#             print("Playing note: ", frequency)

#         # Play the aarohanam of the Mohanam raga
#         for note in message_to_send:
#             play_note(carnatic_notes[note], 2)

#     elif Job == "RECEIVE":
#         Done = False
#         rec_freq = []
#         received_data = []
#         while not Done:
#             fs = 44100
#             duration = 2
#             data = sd.rec(int(fs * duration), fs, channels=1)
#             sd.wait()  # wait for recording to finish
#             # take the FFT of the recorded audio
#             fft_out = fft(data[:, 0])

#             # find the index of the maximum value in the spectrum
#             max_index = np.argmax(np.abs(fft_out))

#             # calculate the frequency of the maximum value
#             frequency = max_index * fs / len(data)
#             print("Receiving:", end=" ")
#             if (frequency > carnatic_notes["Sa"] - 5) and (
#                 carnatic_notes["Sa"] + 5 > frequency
#             ):
#                 print("Sa")
#                 received_data.append("000")
#             elif (frequency > carnatic_notes["Ma1"] - 5) and (
#                 carnatic_notes["Ma1"] + 5 > frequency
#             ):
#                 print("Ma1")
#                 received_data.append("011")
#             elif (frequency > carnatic_notes["Re1"] - 5) and (
#                 carnatic_notes["Re1"] + 5 > frequency
#             ):
#                 print("Re1")
#                 received_data.append("001")
#             elif (frequency > carnatic_notes["Ga3"] - 5) and (
#                 carnatic_notes["Ga3"] + 5 > frequency
#             ):
#                 print("Ga3")
#                 received_data.append("010")
#             elif (frequency > carnatic_notes["Pa"] - 5) and (
#                 carnatic_notes["Pa"] + 5 > frequency
#             ):
#                 print("Pa")
#                 received_data.append("100")
#             elif (frequency > carnatic_notes["Dha1"] - 5) and (
#                 carnatic_notes["Dha1"] + 5 > frequency
#             ):
#                 print("Dha1")
#                 received_data.append("101")
#             elif (frequency > carnatic_notes["Ni3"] - 5) and (
#                 carnatic_notes["Ni3"] + 5 > frequency
#             ):
#                 print("Ni3")
#                 received_data.append("110")
#             elif (frequency > carnatic_notes["SaU"] - 5) and (
#                 carnatic_notes["SaU"] + 5 > frequency
#             ):
#                 print("SaU")
#                 received_data.append("111")
#             else:
#                 print("Nothing")

#             rec_freq.append(frequency)


#             Done = True
#             if len(rec_freq) < 20:
#                 Done = False

#             else:
#                 for a in rec_freq:
#                     if a > 200:
#                         Done = False
#                 rec_freq.pop(0)
        
#         rec_data = ''
#         for strn in received_data:
#             rec_data = rec_data + strn 
#         print("Message received is: {rec_data}")
#     else:
#         break

def receive():
    Job = input("Would you like to TRANSMIT, RECEIVE or END?  ")

    if Job == "TRANSMIT":
        
        bits = input("Type in Binary String to Send: ")
        if len(bits) % 3 == 1:
            bits = bits + "00"
        elif len(bits) % 3 == 2:
            bits = bits + "0"

        print(bits)
        message_to_send = bits_to_notes(bits)
        print(message_to_send)

        # Function to play a note for a given duration
        def play_note(frequency, duration):
            samples = np.arange(44100 * duration)
            note = np.sin(2 * np.pi * frequency * samples / 44100)
            sd.play(note, blocking=True)
            print("Playing note: ", frequency)

        # Play the aarohanam of the Mohanam raga
        for note in message_to_send:
            play_note(carnatic_notes[note], 2)

    elif Job == "RECEIVE":
        Done = False
        rec_freq = []
        received_data = []
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
            if (frequency > carnatic_notes["Sa"] - 5) and (
                carnatic_notes["Sa"] + 5 > frequency
            ):
                print("Sa")
                received_data.append("000")
            elif (frequency > carnatic_notes["Ma1"] - 5) and (
                carnatic_notes["Ma1"] + 5 > frequency
            ):
                print("Ma1")
                received_data.append("011")
            elif (frequency > carnatic_notes["Re1"] - 5) and (
                carnatic_notes["Re1"] + 5 > frequency
            ):
                print("Re1")
                received_data.append("001")
            elif (frequency > carnatic_notes["Ga3"] - 5) and (
                carnatic_notes["Ga3"] + 5 > frequency
            ):
                print("Ga3")
                received_data.append("010")
            elif (frequency > carnatic_notes["Pa"] - 5) and (
                carnatic_notes["Pa"] + 5 > frequency
            ):
                print("Pa")
                received_data.append("100")
            elif (frequency > carnatic_notes["Dha1"] - 5) and (
                carnatic_notes["Dha1"] + 5 > frequency
            ):
                print("Dha1")
                received_data.append("101")
            elif (frequency > carnatic_notes["Ni3"] - 5) and (
                carnatic_notes["Ni3"] + 5 > frequency
            ):
                print("Ni3")
                received_data.append("110")
            elif (frequency > carnatic_notes["SaU"] - 5) and (
                carnatic_notes["SaU"] + 5 > frequency
            ):
                print("SaU")
                received_data.append("111")
            else:
                print("Nothing")

            rec_freq.append(frequency)


            Done = True
            if len(rec_freq) < 20:
                Done = False

            else:
                for a in rec_freq:
                    if a > 200:
                        Done = False
                rec_freq.pop(0)
        
        rec_data = ''
        for strn in received_data:
            rec_data = rec_data + strn 
        print("Message received is: {rec_data}")

def sleep():
    time.sleep(3)

while True:
    t1 = threading.Thread(target=receive)
    t2 = threading.Thread(target = sleep)

    t2.start()
    t1.start()

    t1.join()
    t2.join()