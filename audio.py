import numpy as np
import sounddevice as sd

sample_rate = 44100

phase = 0.0
frequency = 440.0
target_frequency = 440.0

volume = 0.0
target_volume = 0.0


def callback(outdata, frames, time, status):
    global phase
    global frequency
    global target_frequency
    global volume
    global target_volume

    output = np.zeros(frames)

    for i in range(frames):

        frequency += 0.001 * (target_frequency - frequency)
        volume += 0.003 * (target_volume - volume)

        phase += 2 * np.pi * frequency / sample_rate

        if phase > 2 * np.pi:
            phase -= 2 * np.pi

        output[i] = volume * np.sin(phase)

    outdata[:, 0] = output

    if outdata.shape[1] > 1:
        outdata[:, 1] = output


stream = sd.OutputStream(
    samplerate=sample_rate,
    channels=2,
    callback=callback,
)

stream.start()