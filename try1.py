import numpy as np
import sounddevice as sd

# Set the sampling rate and duration of the audio signal
sampling_rate = 44100
duration = 1

# Create a dictionary to map frequencies to corresponding signal
frequencies = {1: 240, 2: 270, 3: 300, 4: 320,
               5: 360, 6: 400, 7: 450, 8: 480}


def scale(frequencies, scale_factor):
    for key, value in frequencies.items():
        frequencies[key] = value*scale_factor


scale(frequencies, 3)

# Create a function to generate audio signal of a specific frequency


def generate_audio(frequency):
    samples = np.linspace(0, duration, int(
        sampling_rate*duration), endpoint=False)
    signal = np.sin(2 * np.pi * frequency * samples)
    return signal

# Create a function to receive and parse audio signal


def receive_and_parse(signal):
    # Perform FFT on the signal to get the frequency content
    frequency_content = np.fft.fft(signal)
    # Get the magnitude of the frequencies
    magnitudes = np.abs(frequency_content[:int(len(frequency_content)/2)])
    # Find the index of the highest magnitude
    highest_magnitude_index = np.argmax(magnitudes)
    print(highest_magnitude_index)
    for key, value in frequencies.items():
        if highest_magnitude_index in range(int(value-20), int(value+20)):
            frequency = value
            return frequency
    print("The received frequency does not match any of the known frequencies")


# Encode 8 different audio frequencies
for i in range(1, 9):
    frequency = frequencies[i]
    signal = generate_audio(frequency)
    sd.play(signal, sampling_rate)
    sd.wait()
    print(f'Playing frequency: {frequency}')

# Receive and parse audio signal
    sd.default.channels = 1
    recording = sd.rec(int(sampling_rate * duration), sampling_rate, channels=1)
    sd.wait()
    frequency = receive_and_parse(recording)
    print("Received frequency:", frequency)
