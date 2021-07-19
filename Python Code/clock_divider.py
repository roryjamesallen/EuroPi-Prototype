"""
Clock Divider
author: awonak
version: 1.0

Provide 4 divisions of the master clock set by knob 1.

knob_1: master clock tempo
digital_1: first division, default master clock
digital_2: second division, default /2
digital_3: third division, default /4
digital_4: fourth division, default /8

"""
from europi import *

import time

MIN_BPM = 20
MAX_BPM = 280

# Useful divisions: [1, 2, 3, 4, 5, 6, 7, 8, 12, 16]
# Length of divisions must not exceed 4 (the number of digital pins).
divisions = [1, 2, 4, 8]

# Start the main loop.
counter = 1
while True:
    # Set the clock speed via Knob 1.
    # tempo range will be between 20 and 280 BPM.
    # Knob 12 o'clock position is 150 BPM.
    tempo = (knob_1.percent() * (MAX_BPM - MIN_BPM)) + MIN_BPM
    time.sleep(60 / tempo)

    # Trigger the digital pin if it's divisible by the counter.
    for i, pin in enumerate([digital_1, digital_2, digital_3, digital_4]):
        if counter % divisions[i] == 0:
            pin.trigger()

    # Wrap the counter if we've reached the largest division.
    if counter == divisions[-1]:
        counter = 1
    else:
        counter += 1

