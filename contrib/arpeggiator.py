"""
Arpeggiator
author: awonak
version: 2.0

Cycle through a sequence of notes in a scale.

Master tempo is set by knob 1, each analog output has a diffent cycle pattern
and each digital output triggers a different rhythmic pattern based off the
master clock. Knob 2 will adjust the octave range from 1 to 3 octaves.

knob_1: adjust the master clock tempo
knob_2: adjust the octave range; 1, 2 or 3 octaves
button_1: reset arpeggio order back to first note in pattern and change scale
analog_1: play notes in ascending order: 1 > 2 > 3
analog_2: play notes in descending order: 3 > 2 > 1
analog_3: play notes in asc & desc order: 1 > 2 > 3 > 3 > 2 > 1
analog_4: play notes in scale will be played randomly
digital_1: master clock trigger
digital_2: trigger at cycle start
digital_3: trigger at sequence step divided by 3
digital_4: trigger at sequence step divided by 4
"""

from europi import *
from random import choice
import time

DEBUG = False
MIN_BPM = 20
MAX_BPM = 500
OCTAVE_RANGE = 3  # EuroPi outputs max 3.3v so we only have a 3 octave range


class Scale:
    """A series of notes in a scale and its sequence state."""

    def __init__(self, notes: tuple(int), include_octave: bool) -> None:
        self.notes = notes
        self.include_octave = include_octave

        self.step = 0
        self.bi_forward = True

    # Scale length for the current selected octave range.
    def __len__(self) -> int:
        length = int((len(self.notes) / OCTAVE_RANGE) * octave_range)
        if self.include_octave:
            length += 1
        return min(length, len(self.notes))

    # Restart the scale sequence.
    def restart(self) -> None:
        self.step = 0
        self.bi_forward = True

    # Proceed to the next step in the scale sequence.
    def next_step(self) -> bool:
        if self.step + 1 == len(self):
            self.step = 0
            self.bi_forward = not self.bi_forward
        else:
            self.step += 1
        return True

    # Calculate the current note for each arpeggio pattern.
    def play(self) -> tuple(int):
        fwd = scale.notes[self.step]
        bwd = scale.notes[0 : len(self)][0 - self.step - 1]
        bi = fwd if self.bi_forward else bwd
        rnd = choice(scale.notes[0 : len(self)])
        return fwd, bwd, bi, rnd


def get_octave_range() -> int:
    """Get the current selected octave range."""
    return int(knob_2.percent() * OCTAVE_RANGE - 0.0001) + 1


# Define the scales available.
scales = [
    Scale(create_scale([1, 3, 5, 6, 8, 10, 12]), True),  # Major scale
    Scale(create_scale([1, 3, 4, 6, 8, 9, 11]), True),  # Minor scale
    Scale(create_scale([1, 5, 8]), False),  # Major triad
    Scale(create_scale([1, 4, 8]), False),  # Minor triad
    Scale(create_scale([1, 3, 5, 6, 8]), False),  # Major pentatonic
    Scale(create_scale([1, 4, 5, 6, 9]), False),  # Minor pentatonic
    Scale(create_scale(range(1, 12)), True),  # Chromatic scale
    Scale(create_scale([1]), True),  # Octave
    Scale(create_scale([1, 12]), False),  # Octave + 7th
]
scale = scales[0]

# Initialize the octave range
prev_octave_range = get_octave_range()
octave_range = prev_octave_range

# Each digital output object.
outputs = [digital_1, digital_2, digital_3, digital_4]


# Handler function for button 1 to cycle to the next scale sequence.
@button_1.handler
def next_scale():
    global scale
    scale = scales[(scales.index(scale) + 1) % len(scales)]
    scale.restart()


# Increment sequence step, or cycle back to the beginning.
while scale.next_step():
    # Set the tempo
    tempo = (knob_1.percent() * (MAX_BPM - MIN_BPM)) + MIN_BPM
    time.sleep((60 / tempo) / 4)

    # Set the octave range
    octave_range = get_octave_range()
    if octave_range != prev_octave_range:
        prev_octave_range = octave_range
        scale.restart()

    # Choose the frequency for each arp direction.
    fwd, bwd, bi, rnd = scale.play()
    analogue_1.value(fwd)
    analogue_2.value(bwd)
    analogue_3.value(bi)
    analogue_4.value(rnd)

    # Activate triggers for this scale sequence step.
    digital_1.value(1)
    if scale.step == 0:
        digital_2.value(1)
    if scale.step % 3 == 0:
        digital_3.value(1)
    if scale.step % 4 == 0:
        digital_4.value(1)

    # Sleep for standard trigger duration and turn off all digital outs.
    time.sleep(0.05)
    [pin.value(0) for pin in outputs]

    if DEBUG:
        msg = "{:>2}) A[1:{:>6} 2:{:>6} 3:{:>6} 4:{:>6}] scale:{:>2} octaves:{:>2} tempo:{}".format(
            scale.step, fwd, bwd, bi, rnd, scales.index(scale), octave_range, tempo
        )
        print(msg)
