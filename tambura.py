import sounddevice as sd
import numpy as np

# The frequency of Sa
sa_frequency = 250

# List of the intervals between the notes of the scale
carnatic_intervals = [1, 256/243, 16/15, 10/9, 9/8, 32/27, 6/5, 5/4, 81/64, 4/3, 729/512, 3/2, 128/81, 8/5, 5/3, 27/16, 7/4, 16/9, 9/5, 15/8, 2]

# Define the sampling rate (fs)
fs = 44100

# List of the names of the notes in the scale
note_names = ['Sa', 'Ri1', 'Ri2', 'Ga1', 'Ga2', 'Ma1', 'Ma2', 'Pa', 'Da1', 'Da2', 'Ni1', 'Ni2', 'Sa']


# Function to generate and play the sound of a note
def play_note(frequency, amplitude, duration):
    # Generate the samples of the sound
    samples = amplitude * np.sin(2 * np.pi * np.arange(44100 * duration) * frequency / 44100)
    # Play the sound
    sd.play(samples, 44100)
    sd.wait()

# Generate the frequencies of the notes in the scale
frequencies = [sa_frequency * carnatic_intervals[i] for i in range(len(carnatic_intervals))]

# Set the amplitude and duration of the sound
amplitude = 0.5
duration = 2

# Play the sound of each note in the scale
for i in range(len(frequencies)):
    print("Playing ",note_names[i])
    play_note(frequencies[i], amplitude, duration)


# Generate the frequencies of the notes in the scale
frequencies = [sa_frequency * carnatic_intervals[i] for i in range(len(carnatic_intervals))]

# Play the sound of each note in the scale
for i in range(len(frequencies)):
    print("Playing ",note_names[i])
    play_note(frequencies[i], amplitude, duration)

