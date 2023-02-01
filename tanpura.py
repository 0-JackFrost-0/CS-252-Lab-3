# import sounddevice as sd
# import numpy as np

# # Define the recording parameters
# fs = 44100  # Sample rate
# duration = 4  # Recording duration in seconds

# # Record audio using sounddevice
# recording = sd.rec(int(fs * duration), fs, channels=1)
# print("Recording...")
# sd.wait()  # Wait until recording is finished

# # Extract the fundamental frequency of the recording
# pitch = np.abs(np.fft.rfft(recording))
# fundamental_frequency = np.argmax(pitch) * fs / len(recording)
# print("Fundamental frequency: {:.2f} Hz".format(fundamental_frequency))

# #generating the 12 notes' frequencies of the classical carntic notes
# s = fundamental_frequency
# r1 = s*pow(2,(2/12))
# r2 = s*pow(2,(5/12))
# g1 = s*pow(2,(7/12))
# g2 = s*pow(2,(9/12))
# m1 = s*pow(2,(11/12))
# m2 = s*pow(2,(14/12))
# p = s*pow(2,(16/12))
# d1 = s*pow(2,(19/12))
# d2 = s*pow(2,(21/12))
# n1 = s*pow(2,(24/12))
# n2 = s*pow(2,(26/12))

# print("12 Classical Carnatic Notes Frequencies:",s,r1,r2,g1,g2,m1,m2,p,d1,d2,n1,n2)


import sounddevice as sd
import numpy as np
from scipy.fftpack import fft

# Define the sample rate and duration of the recording
sample_rate = 44100
duration = 5

# Start recording
recording = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1)
print("Recording...")
sd.wait()
print("Recording finished.")

# Perform FFT on the recording
fft_data = fft(recording)

# Find the index of the maximum value in the FFT data
max_index = np.argmax(np.abs(fft_data))

# Calculate the base frequency of the tanpura drone
base_frequency = max_index * sample_rate / len(recording)

print("Base frequency of the tanpura drone: {:.2f} Hz".format(base_frequency))