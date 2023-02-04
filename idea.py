# This code uses the wave module to read the .wav file and extract the sample rate, number of channels, and number of frames.
#  The wave data is then read as a numpy array, and if the file has multiple channels, the average of all channels is taken.
#  The Fast Fourier Transform (FFT) is then applied to the wave data to find the frequencies, and the indices of the peaks in the frequency spectrum are found. 
# The wave data is then split into segments, each representing a single audio signal, by taking the 
# difference between adjacent samples. 
# The FFT is then applied to each segment to find the frequency of the audio signal, and the duration is 
# calculated based on the length of the segment. The frequency and duration of each audio signal are then added to a list, which is returned as the result.


import wave
import numpy as np
import matplotlib.pyplot as plt
import scipy.fftpack

def extract_frequency_duration(filename):
    # Open the wave file
    wave_file = wave.open(filename, 'r')

    # Extract the sample rate, number of channels, and number of frames
    sample_rate = wave_file.getframerate()
    num_channels = wave_file.getnchannels()
    num_frames = wave_file.getnframes()

    # Read the wave file data as a numpy array
    wave_data = wave_file.readframes(num_frames)
    wave_data = np.frombuffer(wave_data, dtype=np.int16)

    # If the file has multiple channels, take the average of all channels
    if num_channels > 1:
        wave_data = np.mean(wave_data.reshape(-1, num_channels), axis=1)

    # Split the wave data into chunks, each representing a single audio signal
    chunk_size = int(sample_rate * 2) # assume each signal lasts for 2 seconds
    chunks = [wave_data[i:i+chunk_size] for i in range(0, len(wave_data), chunk_size)]

    frequency_duration = []

    for chunk in chunks:
        # Apply FFT to the chunk to find the frequency of the audio signal
        yf = scipy.fftpack.fft(chunk)
        freqs = scipy.fftpack.fftfreq(len(yf), 1/sample_rate)
        idx = np.argmax(np.abs(yf))
        frequency = freqs[idx]

        # Calculate the duration of the audio signal
        duration = len(chunk) / sample_rate

        # Add the frequency and duration to the result list
        frequency_duration.append((frequency, duration))

    return frequency_duration


