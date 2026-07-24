import numpy as np
import sounddevice as sd

sample_rate = 44100

frequency = 440.0
target_frequency = 440.0
phase = 0.0


def callback(outdata, frames, time, status):
    global phase, frequency, target_frequency

    frequency += (target_frequency - frequency) * 0.1

    t = (np.arange(frames) + phase) / sample_rate

    outdata[:, 0] = 0.2 * np.sin(2 * np.pi * frequency * t)

    if outdata.shape[1] > 1:
        outdata[:, 1] = outdata[:, 0]

    phase += frames


stream = sd.OutputStream(
    channels=2,
    callback=callback,
    samplerate=sample_rate,
)

stream.start()