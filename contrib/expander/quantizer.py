from europi import *
from expander import *


class Scale:
    """A series of notes in a scale."""

    def __init__(self, name: str, steps: tuple(int)):
        self.name = name
        self.steps = steps
        self.notes = create_scale(steps)
    
    def get_step(self, note: int) -> str:
        if note == 0:
            return self.steps[0]
        n = self.notes.index(note) % len(self.steps)
        return self.steps[n-1]


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


# Handler function for button to cycle to the next quantizer scale.
@joystick.button_handler
def next_scale():
    global scale
    scale = scales[(scales.index(scale) + 1) % len(scales)]


def quantized_note(value: int, notes: tuple(int)) -> int:
    """Return the nearest quantized note in a chromatic scale."""

    def search(start, end):
        if start + 1 == end:
            return notes[start]

        pivot = int(((end - start) / 2) + start)

        if value < notes[pivot]:
            return search(start, pivot)
        else:
            return search(pivot, end)

    return search(0, len(notes))

while True:
    value = analog_in.value()
    note = quantized_note(value, scale.notes)
    analog_out.value(note)

    oled.fill(0)
    oled.text("Scale:", 0, 0)
    oled.text(scale.name, 0, 12)
    oled.text("V in: {}".format(value), 0, 40)
    oled.text("Step: {}".format(scale.get_step(note)), 0, 52)
    oled.show()
