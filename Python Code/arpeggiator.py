"""
Arpeggiator
author: awonak
version: 1.0

Cycle through a series of notes.

Master tempo is set by knob 1, each analog output has a diffent cycle pattern
and each digital output triggers a different rhythmic pattern based off the
master clock.

knob_1: adjust master clock tempo
button_1: reset arpeggio order back to first note in pattern and change scale
analog_1: play notes in ascending order: 1 > 2 > 3
analog_2: play notes in descending order: 3 > 2 > 1
analog_3: play notes in asc & desc order: 1 > 2 > 3 > 3 > 2 > 1
analog_4: play notes in chord will be played randomly
digital_1: master clock trigger
digital_2: trigger at cycle start
"""

from europi import *
import time

DEBUG = False
MIN_BPM = 20
MAX_BPM = 280
CYCLE_LEN = 8


chords = [c_maj_bass, d_min_bass, d_maj_bass, jazz_bass]
chord = chords[0]
counter = 0
forward = True


# Reset the sequence counter and change to the next chord.
def reset_counter():
    global chord, counter
    counter = 0
    chord = chords[(chords.index(chord)+1) % len(chords)]
button_1.handler(reset_counter)


# Start the main loop.
while True:
    tempo = (knob_1.percent() * (MAX_BPM - MIN_BPM)) + MIN_BPM
    time.sleep((60 / tempo) / 4)

    # Choose the frequency for each arp direction.
    fwd = chord[counter]
    bwd = chord[0-counter-1]
    bi = fwd if forward else bwd
    rnd = choice(chord)

    analogue_1.value(fwd)
    analogue_2.value(bwd)
    analogue_3.value(bi)
    analogue_4.value(rnd)

    digital_1.value(1)

    # Increment or reset counter. Trigger digital 2 on cycle restart.
    if counter+1 == CYCLE_LEN:
        digital_2.value(1)
        counter = 0
        forward = not forward
    else:
        counter += 1

    # Sleep for standard trigger duration and turn off all digital outs.
    time.sleep(0.05)
    digital_1.value(0)
    digital_2.value(0)

    if DEBUG:
        msg = "{})1:{:>8}\t2:{:>8}\t3:{:>8}\t4:{:>8}\tchord:{:>4}\ttempo:{}"
        print(msg.format(counter, fwd, bwd, bi, rnd, chords.index(chord), tempo))
