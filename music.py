import math

SCALES = {
    "Chromatic":  [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
    "Major":      [0, 2, 4, 5, 7, 9, 11],
    "Minor":      [0, 2, 3, 5, 7, 8, 10],
    "Pentatonic": [0, 2, 4, 7, 9],
    "Dorian":     [0, 2, 3, 5, 7, 9, 10],
}


def freq_to_midi(freq):
    return 69 + 12 * math.log2(freq / 440.0)


def midi_to_freq(midi):
    return 440.0 * (2 ** ((midi - 69) / 12.0))


def quantize(freq, scale):

    midi = round(freq_to_midi(freq))

    octave = midi // 12
    note = midi % 12

    allowed = SCALES[scale]

    closest = min(
        allowed,
        key=lambda n: abs(n - note)
    )

    return midi_to_freq(octave * 12 + closest)