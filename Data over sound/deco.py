import sounddevice as sd
from pysinewave import SineWave
import numpy as np
import math
import time
fs = 44100

alphabet = 'abcdefghijklmnopqrstuvwxyz 1234567890.'

stoi = {c: i for i, c in enumerate(alphabet)}
itos = {i: c for i, c in enumerate(alphabet)}

def decode(indices):
    return ''.join([itos[i] for i in indices])
def encode(s):
    return [stoi[c] for c in s]
def frequency_to_pitch(frequency):
    return 9 + 12 * math.log2(frequency / 440)

def record(seconds,ch_sz):
    CR = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
    sd.wait()  
    CR = np.mean(CR, axis=1)
    CR = CR - np.mean(CR)
    chunk_size = int(ch_sz * fs)


    clips = CR.reshape(-1, chunk_size)
    fft_samples = np.abs(np.fft.rfft(clips, axis=1))
    peak_indices = np.argmax(fft_samples, axis=1)
    frequencies = np.fft.rfftfreq(clips.shape[1], 1 / fs)
    return frequencies[peak_indices]
max_frequencies = record(3,1)

T = []
for i in max_frequencies:
    if i<0:
        continue
    fr = round(frequency_to_pitch(i))
    T.append(fr)
T_CR = T
T = decode(T)

print(f"Handshake recieved! {T_CR}")
def confirmation(CR):
    sinewave = SineWave(pitch = 0, pitch_per_second = 1000,decibels=0.1,decibels_per_second=1000)
    sinewave.play()
    for i in CR:
        print(i)
        sinewave.set_pitch(i)
        time.sleep(1)
confirmation(T_CR)
# Make a rebound protocol
while True():
    F_CR = max(record(1,1))
    if F_CR == len(alphabet)+1:
        msg = decode(record(T,0.5))
        print(msg)
        break
    else:
        RT_CR = record(3,1)
        confirmation(RT_CR)








