import time
from pysinewave import SineWave
import sounddevice as sd
import math
from scipy import signal
import numpy as np

fs = 44100 
seconds = 2 
alphabet = 'abcdefghijklmnopqrstuvwxyz 1234567890.'

stoi = {c: i for i, c in enumerate(alphabet)}
itos = {i: c for i, c in enumerate(alphabet)}


def decode(indices):
    return ''.join([itos[i] for i in indices])
def encode(s):
    return [stoi[c] for c in s]
def frequency_to_pitch(frequency):
    return 9 + 12 * math.log2(frequency / 440)
def pitch_to_frequency(frequency):
    return 440 * 2 ** ((frequency - 9) / 12)

#Sound control
text = input("enter text:")
text = encode(list(text))
sinewave = SineWave(pitch = 0, pitch_per_second = 1000,decibels=0.1,decibels_per_second=1000)


#Hand Shake
T = 0
for i in range(len(text)):
    T += 0.5
T = list(str(T))
T = encode(T)

def handshake():

    sinewave.play()
    for i in T:
      
        sinewave.set_pitch(i)
        time.sleep(1)
    sinewave.stop()
handshake()

time.sleep(1)
CT = 0
while True:
    CR = sd.rec(int(3 * fs), samplerate=fs, channels=2)
    sd.wait()  
    CR = np.mean(CR, axis=1)
    CR = CR - np.mean(CR)
    chunk_size = int(1 * fs)

    clips = CR.reshape(-1, chunk_size)
    fft_samples = np.abs(np.fft.rfft(clips, axis=1))
    peak_indices = np.argmax(fft_samples, axis=1)
    frequencies = np.fft.rfftfreq(clips.shape[1], 1 / fs)
    max_frequencies = frequencies[peak_indices]

    CT = []
    for i in max_frequencies:
        if i<0:
            continue
        print(i)
        fr = round(frequency_to_pitch(i))
        CT.append(fr)

    if CT == T:
        print("Handshake Confirmed!")
        sinewave.set_pitch(len(alphabet)+1)
        sinewave.play()
        time.sleep(1)
        sinewave.stop()
        break
    else:
        print("Handshake Failed!")
        sinewave.set_pitch(len(alphabet)+2)
        sinewave.play()
        time.sleep(1)
        sinewave.stop
        handshake()

CR = sd.rec(int(1 * fs), samplerate=fs, channels=2)
sd.wait()  
CR = np.mean(CR, axis=1)
CR = CR - np.mean(CR)
chunk_size = int(1 * fs)

clips = CR.reshape(-1, chunk_size)
fft_samples = np.abs(np.fft.rfft(clips, axis=1))
peak_indices = np.argmax(fft_samples, axis=1)
frequencies = np.fft.rfftfreq(clips.shape[1], 1 / fs)
max_frequencies = frequencies[peak_indices]
max_frequency = frequency_to_pitch(max(max_frequencies))


if max_frequency == len(alphabet)+1:
    sinewave.play
    for i in text:
        if i>= len(alphabet)//2:
            i = -i
        sinewave.set_pitch(i)
        print(i)
        time.sleep(0.5)
else:
    print("No Confirmation Sound Detected")



