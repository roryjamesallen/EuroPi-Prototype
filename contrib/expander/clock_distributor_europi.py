"""
Clock Divider
author: awonak
version: 1.0

Provide 4 divisions of the master clock set by expander Pin(8).

Master clock provided by the expander will emit a trigger pulse once every 
quarter note for the current tempo. Use button 2 to cycle through each digital
out enabling it to set a division from a list of division choices chosen by 
knob 2.

knob_2: choose the division for the current selected index.
button_2: cycle through the digital
digital_1: first division, default /1
digital_2: second division, default /2
digital_3: third division, default /4
digital_4: fourth division, default /8

Expander:
UART(1, tx:4, rx:5): 
    DivisionsState(selected_output, d1, d2, d3, d4)

Pin(8): cv clock output

"""
from europi import knob_2, button_2, digital_1, digital_2, digital_3, digital_4
from machine import Pin, UART
from ustruct import pack
from utime import sleep_ms
from collections import namedtuple


DEBUG = False

# Each digital output object.
OUTPUTS = [digital_1, digital_2, digital_3, digital_4]

# UART serial communication
uart1 = UART(1, baudrate=115200, tx=Pin(4), rx=Pin(5))

# Digital pin to read input clock from the expander.
clock_pin = Pin(8, Pin.IN, Pin.PULL_DOWN)
prev_clock = 0

# Divisions state struct.
DivisionsState = namedtuple("DivisionsState", "selected_output d1 d2 d3 d4")
format_string = "5b"


class Divisions:
    # Useful divisions to choose from.
    DIVISION_CHOICES = [1, 2, 3, 4, 5, 6, 7, 8, 12, 16]
    MAX_DIVISION = max(DIVISION_CHOICES)

    def __init__(self, control_pin:Pin, control_button:Pin, divisions: tuple(int)):
        # Input controls
        self.k = control_pin
        control_button.handler(self.select_next_division)

        # Divisions corresponding to each digital output.
        self.divisions = divisions

        # Selects the Digital Jack to adjust clock division using 0-based index with an
        # extra index to disable config controls.
        self.selected_output = -1
        self._previous_choice = -1

        # Clock divider iteration counter.
        self.counter = 0
    
    @property
    def _state(self):
        return pack(format_string, self.selected_output, *self.divisions)

    def select_next_division(self):
        self.selected_output += 1
        if self.selected_output == len(self.divisions):
            self.selected_output = -1  # Disable division config
        # Send state to expander.
        uart1.write(self._state)
    
    def get_division_choice(self):
        return int(self.k.percent() * len(self.DIVISION_CHOICES) - 0.0001)
    
    def adjust_division(self):
        choice = self.get_division_choice()
        if self.selected_output >= 0 and choice != self._previous_choice:
            self.divisions[self.selected_output] = self.DIVISION_CHOICES[choice]
            self._previous_choice = choice
            # Send state to expander.
            uart1.write(self._state)
    
    def trigger(self):
        for i, pin in enumerate(OUTPUTS):
            if self.counter % self.divisions[i] == 0:
                pin.value(1)
        sleep_ms(10)
        [pin.value(0) for pin in OUTPUTS]

        # Wrap the counter if we've reached the largest division.
        # self.counter = (self.counter + 1) % divisions.MAX_DIVISION
        self.counter += 1
    
    def debug(self) -> str:
        return 'DJ: {self.divisions}  || config:{self.selected_output}'.format(self)


divisions = Divisions(knob_2, button_2, [1, 2, 4, 8])


def clock_wait():
    # Wait for clock pulse to advance.
    global prev_clock
    while True:
        if clock_pin.value() != prev_clock:
            prev_clock = 1 if prev_clock == 0 else 0
            if prev_clock == 0:
                return


# Start the main loop.
while True:
    # Wait for the next click pulse.
    clock_wait()

    # Trigger the digital pin if it's divisible by the counter.
    divisions.trigger()

    # Set the currently selected digital out's clock division to the value
    # selected by knob 2.
    divisions.adjust_division()  # TODO: this should be async

    if DEBUG:
        print(divisions.debug())
