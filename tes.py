import librosa

y, sr = librosa.load(librosa.ex('choice'), duration=10)
tempo, beats = librosa.beat.beat_track(y=y, sr=sr)
print(tempo)
135.99917763157896
#Print the frames corresponding to beats

print(beats)
#Or print them as timestamps

print(librosa.frames_to_time(beats, sr=sr))
# array([0.07 , 0.488, 0.929, 1.37 , 1.811, 2.229, 2.694, 3.135,
#        3.576, 4.017, 4.458, 4.899, 5.341, 5.782, 6.223, 6.664,
#        7.105, 7.546, 7.988, 8.429])