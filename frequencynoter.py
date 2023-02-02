
import sounddevice as sd
import numpy as np
import essentia.standard as ess
from scipy.io.wavfile import write

fs = 44100  # Sample rate
duration = 10  # Duration of recording in seconds

# Record audio
print("Listening for Taalam...")
recording = sd.rec(int(fs * duration), samplerate=fs, channels=2)
sd.wait()
print("Processing taalam...")


write('output.wav', fs, recording)  # Save as WAV file

import librosa

# Load audio file
y, sr = librosa.load("output.wav")

# Extract pitch
pitch = librosa.pitch.estimate_tuning(y=y, sr=sr)
print(pitch)
# Convert pitch to MIDI note number
note_number = librosa.hz_to_midi(pitch)

# Convert MIDI note number to note name
note_name = librosa.midi_to_note(note_number)

# Print note name
print("Note:", note_name)
# from music21 import *
# def pitch_to_note_name(pit):
#     note_num = pitch.Pitch(pit)
#     note_name = note.Note(note_num)
#     return note_name.nameWithOctave
# print(pitch)
# import essentia.standard as ess

# # Load audio file
# audio = ess.MonoLoader(filename = 'output.wav')()

# # Detect pitch using PitchYinFFT algorithm
# pitch_detector = ess.PitchYinFFT()
# pitch1, confidence = pitch_detector(audio)
# print(pitch1, confidence)
# # Map pitch to note name in the Western scale
# note_name = pitch_to_note_name(pitch1)

# print("Detected note: ", note_name)