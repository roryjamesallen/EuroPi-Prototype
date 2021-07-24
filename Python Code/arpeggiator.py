"""
Arpeggiator
author: awonak
version: 2.0

Cycle through a series of notes.

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
OCTAVE_RANGE = 3

# Define the scales available.
scales = [
    create_scale([1, 3, 5, 6, 8, 10, 11, 12]),  # Major scale
    create_scale([1, 3, 4, 6, 8, 9, 11, 12]),  # Minor scale
    create_scale([1, 5, 8]),  # Major triad
    create_scale([1, 4, 8]),  # Minor triad
    create_scale([1, 3, 5, 6, 8]),  # Major pentatonic
    create_scale([1, 4, 5, 6, 9]),  # Minor pentatonic
    create_scale([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]),  # Chromatic scale
    create_scale([1, 12, 23, 34]),  # 4 Octave
]
scale = scales[0]

# Initialize the octave range
prev_octave_range = int(knob_2.percent() * OCTAVE_RANGE - 0.0001)

# Each digital output object.
outputs = [digital_1, digital_2, digital_3, digital_4]

# Current direction of the bi-directional analogue output
forward = True

counter = 0


# Reset the sequence counter and change to the next scale.
def reset_counter():
    global scale, counter
    counter = 0
    scale = scales[(scales.index(scale) + 1) % len(scales)]


button_1.handler(reset_counter)


# Start the main loop.
while True:
    # Set the tempo
    tempo = (knob_1.percent() * (MAX_BPM - MIN_BPM)) + MIN_BPM
    time.sleep((60 / tempo) / 4)

    # Set the octave range
    octave_range = int(knob_2.percent() * OCTAVE_RANGE - 0.0001) + 1
    if octave_range != prev_octave_range:
        prev_octave_range = octave_range
        counter = 0

    # Choose the frequency for each arp direction.
    fwd = scale[counter]
    bwd = scale[0 - counter - 1]
    bi = fwd if forward else bwd
    rnd = choice(scale)

    analogue_1.value(fwd)
    analogue_2.value(bwd)
    analogue_3.value(bi)
    analogue_4.value(rnd)

    digital_1.value(1)
    if counter % 3 == 0:
        digital_3.value(1)
    if counter % 4 == 0:
        digital_4.value(1)

    if DEBUG:
        msg = "{:>2})1:{:>8}\t2:{:>8}\t3:{:>8}\t4:{:>8}\tscale:{:>4}\ttempo:{}"
        print(msg.format(counter, fwd, bwd, bi, rnd, scales.index(scale), tempo))

    # Increment or reset counter. Trigger digital 2 on cycle restart.
    if counter + 1 == (len(scale) / OCTAVE_RANGE) * octave_range:
        digital_2.value(1)
        counter = 0
        forward = not forward
    else:
        counter += 1

    # Sleep for standard trigger duration and turn off all digital outs.
    time.sleep(0.05)
    [pin.value(0) for pin in outputs]
