import numpy as np
import sounddevice as sd
import math

sample_rate = 44100

phase = 0.0

frequency = 440.0
target_frequency = 440.0

volume = 0.2
target_volume = 0.2

# cutoff in Hz
cutoff = 1000.0
target_cutoff = 1000.0

# filter state
lp = 0.0


def callback(outdata, frames, time, status):
    global phase
    global frequency
    global target_frequency
    global volume
    global target_volume
    global cutoff
    global target_cutoff
    global lp

    output = np.zeros(frames)

    for i in range(frames):

        # Smooth parameters
        frequency += 0.002 * (target_frequency - frequency)
        volume += 0.01 * (target_volume - volume)
        cutoff += 0.01 * (target_cutoff - cutoff)

        # Phase
        phase += frequency / sample_rate

        if phase >= 1.0:
            phase -= 1.0

        # Sawtooth oscillator
        osc = 2.0 * phase - 1.0

        # One-pole low-pass
        alpha = 1.0 - math.exp(-2.0 * math.pi * cutoff / sample_rate)
        lp += alpha * (osc - lp)

        output[i] = volume * lp

    outdata[:, 0] = output

    if outdata.shape[1] > 1:
        outdata[:, 1] = output


stream = sd.OutputStream(
    samplerate=sample_rate,
    channels=2,
    callback=callback,
)

stream.start()