import numpy as np
import sounddevice as sd
import wave

# Define octal frequencies
octal_frequencies = [1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000]

# Encoding function
def msfk_encode(message, frequencies):
    encoded_message = []
    for char in message:
        binary_char = bin(ord(char))[2:].zfill(8) # Convert character to binary
        for bit, frequency in zip(binary_char, frequencies):
            if bit == '1':
                encoded_message.append(frequency)
            else:
                encoded_message.append(0)
    return encoded_message

# Decoding function
def msfk_decode(encoded_message, frequencies):
    decoded_message = ""
    message_bits = ""
    for frequency in encoded_message:
        if frequency in frequencies:
            message_bits += '1'
        else:
            message_bits += '0'
        if len(message_bits) == 8:
            decoded_message += chr(int(message_bits, 2))
            message_bits = ""
    return decoded_message

# Function to play and record sound
def play_and_record(encoded_message):
    # Define recording parameters
    fs = 44100  # Sample rate
    duration = len(encoded_message)  # Duration of recording

    # Play encoded message
    encoded_message = np.array(encoded_message,dtype=np.float32)
    print(type(encoded_message))
    print(type(fs))
    sd.play(encoded_message, fs)
    print("Playing encoded message...")
    sd.wait()  # Wait for sound to finish playing

    # Record encoded message
    print("Recording encoded message...")
    recorded_message = sd.rec(int(fs * duration), fs, channels=1)
    sd.wait()  # Wait for recording to finish

    # Write recorded message to a wav file
    wavfile = wave.open("recorded_message.wav", "w")
    wavfile.setparams((1, 2, fs, 0, "NONE", "not compressed"))
    wavfile.writeframes(recorded_message.tobytes())
    wavfile.close()
    print("Recorded message saved to recorded_message.wav")

    return recorded_message

# Test the functions
message = "0101"
encoded_message = msfk_encode(message, octal_frequencies)
print("Encoded message:", encoded_message)

recorded_message = play_and_record(encoded_message)

decoded_message = msfk_decode(recorded_message, octal_frequencies)
print("Decoded message:", decoded_message)
