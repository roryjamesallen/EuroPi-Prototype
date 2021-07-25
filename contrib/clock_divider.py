"""
Clock Divider
author: awonak
version: 1.0

Provide 4 divisions of the master clock set by knob 1.

Master clock set by knob 1 will emit a trigger pulse once every quarter note
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
DIVISION_CHOICES = [1, 2, 3, 4, 5, 6, 7, 8, 12, 16]
MAX_DIVISION = max(DIVISION_CHOICES)

# Divisions corresponding to each digital output.
divisions = [1, 2, 4, 8]

# Each digital output object.
outputs = [digital_1, digital_2, digital_3, digital_4]

selected_output = -1
previous_choice = int(knob_2.percent() * len(DIVISION_CHOICES) - 0.0001)
counter = 1


@button_2.handler
def config_divisions():
    global selected_output
    selected_output = (selected_output + 1) % len(divisions)


# Start the main loop.
while True:
    # Set the clock speed via Knob 1.
    # tempo range will be between 20 and 280 BPM.
    # Knob 12 o'clock position is 150 BPM.
    tempo = round((knob_1.percent() * (MAX_BPM - MIN_BPM)) + MIN_BPM, 1)
    # Sleep for a quarter note of the tempo.
    time.sleep((60 / tempo) / 4)

    # Trigger the digital pin if it's divisible by the counter.
    for i, pin in enumerate(outputs):
        if counter % divisions[i] == 0:
            pin.value(1)
    time.sleep(0.05)
    [pin.value(0) for pin in outputs]

    # Set the currently selected digital out's clock division to the value
    # selected by knob 2.
    choice = int(knob_2.percent() * len(DIVISION_CHOICES) - 0.0001)
    if selected_output >= 0 and choice != previous_choice:
        divisions[selected_output] = DIVISION_CHOICES[choice]
        previous_choice = choice

    # Wrap the counter if we've reached the largest division.
    counter = (counter + 1) % MAX_DIVISION

    if DEBUG:
        msg = "DJ: {}  || config:{}  tempo:{}"
        print(msg.format(divisions, selected_output, tempo))
