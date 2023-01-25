import numpy as np
import sounddevice as sd
from scipy import signal

# Set the sampling rate and duration of the audio signal
sampling_rate = 44100
duration = 2
threshold = 0.5

# Create a dictionary to map frequencies to corresponding signal
frequencies = {1: 240, 2: 270, 3: 300, 4: 320,
               5: 360, 6: 400, 7: 450, 8: 480}

# Create a function to generate audio signal of a specific frequency
def generate_audio(frequency):
    samples = np.linspace(0, duration, int(sampling_rate*duration), endpoint=False)
    signal = np.sin(2 * np.pi * frequency * samples)
    return signal

# Create a function to receive and parse audio signal
def receive_and_parse(signal, threshold=0.5):
    # Applying Hann Window
    window = signal.hann(len(signal))
    signal = signal * window
    # Perform FFT on the signal to get the frequency content
    frequency_content = np.fft.fft(signal)[:int(len(signal)/2)]
    # Get the magnitude of the frequencies
    magnitudes = np.abs(frequency_content)
    # Find the index of the highest magnitude
    highest_magnitude_index = np.argmax(magnitudes)
    if magnitudes[highest_magnitude_index] > threshold:
        # Lookup the corresponding frequency from the dictionary
        for freq, index in frequencies.items():
            if index == highest_magnitude_index:
                return freq
    return None

# Encode 8 different audio frequencies
for i in range(1, 9):
    frequency = frequencies[i]
    signal = generate_audio(frequency)
    sd.play(signal, blocking=True)
    recording = sd.rec(int(sampling_rate * duration), sampling_rate, channels=1)
    received_frequency = receive_and_parse(recording, threshold)
    if received_frequency is not None:
        if received_frequency == frequency:
            print(f"Sent frequency {frequency} and received frequency {received_frequency} matched.")
        else:
            print(f"Sent frequency {frequency} but received frequency {received_frequency}.")
    else:
        print("Frequency not found or too low signal.")