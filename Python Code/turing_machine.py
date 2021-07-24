"""
Turing Machine
author: roryjamesallen
version: 1.1

Play a sequence that changes notes within a scale according to the probability set by knob 2.

Use knob 1 to adjust the master clock tempo. The second knob increases the
probability that a note within the sequence will get changed on each step.
The first two analogue jacks play a quantized pitch while the last two
analogue jacks will play a random cv value. Digital 1 will trigger each step,
while digital 2 plays a gate for the duration of the step. Digital 3 will
trigger if a note is changed in the current step and digital 4 will trigger
when the sequence restarts.

knob_1: set master clock tempo
knob_2: set new note chance
button_1: introduce a new note
button_2: lock sequence
analogue_1: 1V/Oct pitch or timbre control
analogue_2: 1V/Oct pitch or timbre control
analogue_3: random cv
analogue_4: random cv
digital_1: trigger
digital_2: gate
digital_3: note changed
digital_4: sequence reset
"""

from europi import *
from random import randint, choice

# Constants
DEBUG = False  # Print debug statements to the console during development
SCALE = d_maj  # Set the scale used by the Turing Machine
SEQUENCE_LENGTH = 8  # You can change this length, 8 is standard

# Variables
sequence = []  # The sequence starts off as an empty array
note = 0  # The index of the currently playing note in the sequence array
lock = False  # A boolean that locks whether new notes can be created


@button_1.handler  # Assign the push_new_note function to button 1
def push_new_note():
    if DEBUG: print("Interrupt Detected!")
    global sequence  # Gives access to the sequence so it can insert the new note
    sequence[note] = new_note  # Inserts a new note the same way it would happen naturally
    digital_3.value(1)  # Sets digital_3 high as this is the jack which indicates a new note has been created


@button_2.handler  # Assign the push_lock function to button 2
def push_lock():
    if DEBUG: print("Interrupt Detected!")
    global lock  # Gives access to the variable lock
    lock = not lock  # Switches lock from either True to False or False to True


class TuringNote:
    """This object will contain the pins used for the note, and methods to allow the note to be played."""
    
    def __repr__(self):
        return "Note: {:>6}".format(self.pitch_1)
    
    def __init__(self, clock, trigger_pin, gate_pin, pitch1_pin, pitch2_pin, timbre1_pin, timbre2_pin): #The pins used by the note are passed in when it is created
        self.trigger_pin = trigger_pin
        self.gate_pin = gate_pin
        self.pitch1_pin = pitch1_pin
        self.pitch2_pin = pitch2_pin
        self.timbre1_pin = timbre1_pin
        self.timbre2_pin = timbre2_pin

        self.length = clock
        self.pitch_1 = choice(SCALE)  # Change this scale to any of the available scales in the europi library or create your own (or set to randint(0,65535) to make it unquantised)
        self.pitch_2 = choice(SCALE)  # Pitch 2 can be used for an alternating melody on a separate oscillator, but it's also useful as a general timbre control
        self.timbre1 = randint(0, UINT_16)  # The timbre is fully randomised to get the full range
        self.timbre2 = randint(0, UINT_16)  # The timbre is fully randomised to get the full range

    # A method to play the note using the jacks specified in the initialisation method
    def play(self):
        self.pitch1_pin.value(self.pitch_1)  # The pitch and timbre pins are all set first to avoid the short slew being heard
        self.pitch2_pin.value(self.pitch_2)
        self.timbre1_pin.value(self.timbre1)
        self.timbre2_pin.value(self.timbre2)

        self.gate_pin.value(1)  # The gate is turned on as this is 'open' the whole time the note is active
        self.trigger_pin.value(1)  # The trigger pin is turned on

        sleep(0.05)  # For 0.05seconds, within the Eurorack standard length
        self.trigger_pin.value(0)  # The trigger pin is turned off

        sleep(abs(self.length - 0.05))  # The note 'sleeps' for the step length minus the trigger time which has already happened
        self.gate_pin.value(0)  # Finally the gate is turned off again


while True:  # The main program runs forever
    clock = (1 - knob_1.percent()) + 0.01  # The clock calculation from knob 1. This gives you a time to sleep value between 0 seconds and 1 second. A very small value (0.01) is added to prevent it from breaking
    digital_4.value(0)  # The sequence has started again, so the reset indicator is turned off

    new_note = TuringNote(clock, digital_1, digital_2, analogue_1, analogue_2, analogue_3, analogue_4)  # A new note is created each time
    if len(sequence) == SEQUENCE_LENGTH:  # The new note can only be swapped out if the sequence has reached its final length, so not for the first x steps
        if random_chance(knob_2.percent()):  # The note is then dependent on the random chance controlled by knob 2
            if lock == False:  # And finally, only if the new note creation is not locked according to button 2
                sequence[note] = new_note  # If all these conditions are met, the note is added to the sequence at the current location
                digital_3.value(1)  # The jack to indicate a new note has been added is turned on
    else:
        sequence.append(new_note)  # If the sequence hasn't yet reached its full length, the note is added to the end

    sequence[note].play()  # The current note is played
    digital_3.value(0)  # The jack to indicate a new note is turned off as the note is over

    note += 1  # The index for sequence is incremented to move on to the next note
    if note == SEQUENCE_LENGTH:  # If the note is at the end of the sequence
        note = 0  # It is reset to the start
        digital_4.value(1)  # And the reset pin turned on to indicate this

    sleep(clock)  # Finally, the time between notes is waited, as controlled by knob 1

    if DEBUG:
        print("Seq: {} Clock: {}".format(sequence, clock))
