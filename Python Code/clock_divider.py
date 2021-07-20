"""
Clock Divider
author: awonak
version: 1.0

Provide 4 divisions of the master clock set by knob 1.

Master clock (divide by 1) will emit a trigger pulse once every quarter note
for the current tempo. Use button 2 to cycle through each digital out enabling
it to set a division from a list of division choices chosen by knob 2.

knob_1: master clock tempo
knob_2: choose the division for the current selected index.
button_2: cycle through the digital
digital_1: first division, default master clock
digital_2: second division, default /2
digital_3: third division, default /4
digital_4: fourth division, default /8

"""
from europi import *

import time

DEBUG = False

MIN_BPM = 20
MAX_BPM = 280

# Useful divisions to choose from.
division_choices = [1, 2, 3, 4, 5, 6, 7, 8, 12, 16]
MAX_DIVISION = max(division_choices)

# Divisions corresponding to each digital output.
divisions = [1, 2, 4, 8]

# Each digital output object.
outputs = [digital_1, digital_2, digital_3, digital_4]

config_index = -1


def config_divisions():
    global config_index
    config_index = (config_index + 1) % len(divisions)
    if DEBUG:
        print("New division config index: ", config_index)
button_2.handler(config_divisions)


# Provide a list of pins to trigger in sync.
def sync_trigger(pins):
    [pin.value(1) for pin in pins]
    time.sleep(0.05)
    [pin.value(0) for pin in pins]


# Start the main loop.
counter = 1
while True:
    # Set the clock speed via Knob 1.
    # tempo range will be between 20 and 280 BPM.
    # Knob 12 o'clock position is 150 BPM.
    tempo = (knob_1.percent() * (MAX_BPM - MIN_BPM)) + MIN_BPM
    # Sleep for a quarter note of the tempo.
    time.sleep((60 / tempo) / 4)

    # Trigger the digital pin if it's divisible by the counter.
    pins = []
    for i, pin in enumerate(outputs):
        if counter % divisions[i] == 0:
            pins.append(pin)
    sync_trigger(pins)

    # Change the current config index digital pin to a division chosen by the
    # current knob 2 value.
    choice = int(knob_2.percent() * len(division_choices) - 0.0001)
    if config_index >= 0 and division_choices[choice] != divisions[config_index]:
        divisions[config_index] = division_choices[choice]

        if DEBUG:
            print("Change DJ{} division to: {}".format(config_index, division_choices[choice]))

    # Wrap the counter if we've reached the largest division.
    counter = (counter + 1) % MAX_DIVISION

    if DEBUG:
        print("DJ: {}  || config:{}  tempo:{}".format(divisions, config_index, tempo))

