"""
Clock Divider
author: awonak
version: 1.1

Provide 4 divisions of the master clock set by expander Pin(8).

Master clock provided by the expander will emit a trigger pulse once every
quarter note for the current tempo. Use button 2 to cycle through each digital
out enabling it to set a division from a list of division choices chosen by
knob 2.

knob_1: internal master clock tempo
knob_2: choose the division for the current selected index.
button_1: switch between internal or external clock source.
button_2: cycle through the digital
digital_1: first division, default /1
digital_2: second division, default /2
digital_3: third division, default /4
digital_4: fourth division, default /8


Expander:

# UART serial communication with expander
UART(1, tx:4, rx:5):
    DivisionsState(selected_output, d1, d2, d3, d4)

# Digital pin to read input clock from the expander.
Pin(8): cv clock output

"""
import europi
from machine import Pin, UART
from ustruct import pack
from utime import sleep_ms
from lib.clock import Clock
from collections import namedtuple


DEBUG = True

# Each digital output object.
OUTPUTS = [europi.digital_1, europi.digital_2, europi.digital_3, europi.digital_4]

# Divisions state struct.
DivisionsState = namedtuple("DivisionsState", "selected_output d1 d2 d3 d4")
format_string = "5b"

# UART serial communication with expander
uart1 = UART(1, baudrate=115200, tx=Pin(4), rx=Pin(5))


class Divisions:
    # Useful divisions to choose from.
    DIVISION_CHOICES = [1, 2, 3, 4, 5, 6, 7, 8, 12, 16]
    MAX_DIVISION = max(DIVISION_CHOICES)

    def __init__(self, clock: Clock, control_pin: Pin, control_button: Pin, divisions: tuple(int)):
        # Input controls
        self.k = control_pin
        control_button.handler(self.select_next_division)

        # Clock source object.
        self.clock = clock

        # Divisions corresponding to each digital output.
        self.divisions = divisions

        # Counters for each clock division (use a copy of the values, not the reference)
        self.counters = divisions[:]

        # Selects the Digital Jack to adjust clock division using 0-based index with an
        # extra index to disable config controls.
        self.selected_output = -1
        self._previous_choice = -1

    @property
    def _state(self):
        """Wire friendly message of the current Divisions state."""
        return pack(format_string, self.selected_output, *self.divisions)

    def select_next_division(self):
        """Cycle through each digital jack to configure it's division."""
        self.selected_output += 1
        if self.selected_output == len(self.divisions):
            self.selected_output = -1  # Disable division config
        # Send state to expander.
        uart1.write(self._state)

    def get_division_choice(self):
        """Get a knob reading to choose a division from the list of choices."""
        return int(self.k.percent() * len(self.DIVISION_CHOICES) - 0.0001)

    def adjust_division(self):
        """When a digital jack is selected, read division choice and update it's division."""
        if self.selected_output >= 0:
            choice = self.get_division_choice()
            if choice != self._previous_choice:
                self.divisions[self.selected_output] = self.DIVISION_CHOICES[choice]
                self._previous_choice = choice
                # Send state to expander.
                uart1.write(self._state)

    def trigger(self):
        """Emit a trigger for each digital jack within this clock cycle."""
        for i, pin in enumerate(OUTPUTS):
            self.counters[i] -= 1
            if self.counters[i] == 0:
                pin.value(1)
                # Reset counter for this division
                self.counters[i] = self.divisions[i]
        sleep_ms(10)
        [pin.value(0) for pin in OUTPUTS]
    
    def run(self) -> None:
        """Run this script in an infinite loop."""
        # Start the main loop.
        while True:
            # Wait for the next click pulse.
            self.clock.wait()

            # Trigger the digital pin if it's divisible by the counter.
            self.trigger()

            # Set the currently selected digital out's clock division to the value
            # selected by knob 2.
            self.adjust_division()  # TODO: this should be async

            if DEBUG:
                print(self.debug())

    def debug(self) -> str:
        msg = 'DJ: {}  || Counts: {}  || config: {} || tempo: {}'
        return msg.format(self.divisions, self.counters, self.selected_output, self.clock.tempo)


divisions = Divisions(
    # Define the clock source
    Clock(europi.knob_1, europi.button_1, Pin(8, Pin.IN, Pin.PULL_DOWN)),
    # Division input controls
    europi.knob_2, europi.button_2,
    # Default divisions
    [1, 2, 4, 8],
)


if __name__ == '__main__':
    divisions.run()
