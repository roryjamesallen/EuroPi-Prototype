"""
Quantizer
author: awonak
version: 1.0

Quantize analog cv input to a configured scale.

{Long description}

knob_1: {knob_1 description}
knob_2: {knob_2 description}
button_1: Change scale
button_2: {button_2 description}
analog_1: {analog_1 description}
analog_2: {analog_2 description}
analog_3: {analog_3 description}
analog_4: {analog_4 description}
digital_1: {digital_1 description}
digital_2: {digital_2 description}
digital_3: {digital_3 description}
digital_4: {digital_4 description}
"""

from machine import Pin, ADC
from europi import analogue_1, button_1, create_scale


DEBUG = True


class AnalogInput:
    def __init__(self, pin: Pin):
        self.pin = ADC(pin)

    def value(self) -> int:
        """Read the received voltage as uint16 value between 0 and 65535."""
        return self.pin.read_u16()

    def percent(self) -> float:
        """Read the current relative voltage returned as a float between 0 and 1."""
        return self.pin.read_u16() / 65535


class DigitalInput:
    def __init__(self, pin: Pin):
        self.pin = pin

    def value(self) -> int:
        """Read the digital pin, HIGH (1) or LOW (0)."""
        return self.pin.value()


class Scale:
    """A series of notes in a scale."""

    def __init__(self, name: str, steps: tuple(int)):
        self.name = name
        self.steps = steps
        self.notes = create_scale(steps, 37)
    
    def get_step(self, note: int) -> int:
        if note == 0:
            return self.steps[0]
        n = self.notes.index(note) % len(self.steps)
        return self.steps[n-1]

    def get_octave(self, note: int) -> int:
        octaves = len(self.notes) / 3
        return int((self.notes.index(note) - 0.1) / octaves) + 1


# Define the scales available.
scales = [
    Scale("Major scale", [1, 3, 5, 6, 8, 10, 12]),
    Scale("Minor scale", [1, 3, 4, 6, 8, 9, 11]),
    Scale("Major triad", [1, 5, 8]),
    Scale("Minor triad", [1, 4, 8]),
    Scale("Major pentatonic", [1, 3, 5, 6, 8]),
    Scale("Minor pentatonic", [1, 4, 5, 6, 9]),
    Scale("Chromatic scale", range(1, 13)),
    Scale("Octave", [1]),
    Scale("Octave + 7th", [1, 12]),
]
scale = scales[0]


# Analog & Digital input jacks
analog_in = AnalogInput(Pin(26))
digital_in = DigitalInput(Pin(2, Pin.IN, Pin.PULL_DOWN))


# Handler function for button to cycle to the next quantizer scale.
@button_1.button_handler
def next_scale():
    global scale
    scale = scales[(scales.index(scale) + 1) % len(scales)]


def quantized_note(value: float) -> int:
    """Return the nearest quantized note in the given scale for the given."""
    index = int((value - 0.001) * len(scale.notes))
    return scale.notes[index]


while True:
    value = analog_in.percent()
    note = quantized_note(value)
    analogue_1.value(note)
    if DEBUG:
        print("Scale: {}\tV in: {}\tStep: {}\tOct: {}", scale.name, value, scale.get_step(note), scale.get_octave(note))
        from utime import sleep_ms; sleep_ms(200)  

