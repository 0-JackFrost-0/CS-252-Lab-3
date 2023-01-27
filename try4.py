import sounddevice as sd
import numpy as np
from scipy.fftpack import fft
import bluetooth

bd_addr = "d8:aa:59:69:f7:1c"

# # connect to the microphone
# port = 1
# sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
# sock.connect((bd_addr, port))

# define the recording parameters
fs = 44100  # sample rate
duration = 1  # in seconds


while True:
# record audio
    data = sd.rec(int(fs * duration), fs, channels=1)
    sd.wait()  # wait for recording to finish

    # take the FFT of the recorded audio
    fft_out = fft(data[:, 0])

    # find the index of the maximum value in the spectrum
    max_index = np.argmax(np.abs(fft_out))

    # calculate the frequency of the maximum value
    frequency = max_index * fs / len(data)

    print("Frequency of sound: ",frequency)

