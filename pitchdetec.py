from pydub import AudioSegment
from pitch_detect import get_pitch

# Load audio file
audio = AudioSegment.from_file("output.wav")

# Extract the audio data as a NumPy array
audio_data = audio.get_array_of_samples()

# Get the pitch of the audio using the get_pitch function
pitch = get_pitch(audio_data, sr=audio.frame_rate)

# Compare the pitch to the reference pitch for a guitar or ukulele
reference_pitch = 440 # A4 for guitar or ukulele
pitch_diff = pitch - reference_pitch

# Adjust the tuning of the guitar or ukulele based on the pitch difference
if pitch_diff > 0:
    print("Tune the instrument down by", pitch_diff, "Hz")
elif pitch_diff < 0:
    print("Tune the instrument up by", abs(pitch_diff), "Hz")
else:
    print("The instrument is in tune!")







