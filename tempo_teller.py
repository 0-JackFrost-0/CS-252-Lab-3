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

# Load the audio into Essentia
audio = ess.MonoLoader(filename="output.wav", sampleRate=fs)()

# Compute beat positions and BPM.
rhythm_extractor = ess.RhythmExtractor2013(method="multifeature")



bpm, beats, beats_confidence, _, beats_intervals = rhythm_extractor(audio)



print("BPM:", bpm)
print("Beat positions (sec.):", beats)
# print("Beat estimation confidence:", beats_confidence)

