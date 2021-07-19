"""
Arpeggiator
author: awonak
version: 1.0

Cycle through a series of notes.

Master tempo is set by knob 1, each analog output has a diffent cycle pattern 
and each digital output triggers a different rhythmic pattern based off the 
master clock.

knob_1: master clock tempo
knob_2: chord quality selector.
button_1: reset arpeggio order back to first note in pattern
analog_1: notes in ascending order: 1 > 2 > 3 
analog_2: notes in descending order: 3 > 2 > 1
analog_3: notes in asc & desc order: 1 > 2 > 3 > 2 > 1
analog_4: notes in chord will be played randomly
digital_1: master clock set by knob 1
"""

from europi import *
import time

MIN_BPM = 20
MAX_BPM = 280
CYCLE_LEN = 8
DEBUG = True

def reset_counter():
    print("Interrupt Detected!")
    global counter
    counter = 0

button_1.handler(reset_counter)

chord = choice([c_maj_bass, d_min_bass, d_maj_bass])
counter = 0
forward = True

# Start the main loop.
while True:
    tempo = (knob_1.percent() * (MAX_BPM - MIN_BPM)) + MIN_BPM
    time.sleep(60 / tempo)
    
    fwd = chord[counter]
    bwd = chord[0-counter-1]
    bi = fwd if forward else bwd
    rnd = choice(chord)
    
    analogue_1.value(fwd)
    analogue_2.value(bwd)
    analogue_3.value(bi)
    analogue_4.value(rnd)

    digital_1.trigger()
    
    if DEBUG:
        print("{})1:{:>8}\t2:{:>8}\t3:{:>8}\t4:{:>8} ".format(counter, fwd, bwd, bi, rnd))

    if counter+1 == CYCLE_LEN:
        counter = 0
        forward = not forward
    else:
        counter += 1

