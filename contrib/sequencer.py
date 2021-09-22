"""
Sequencer

8 step sequencer with programmable pitch and velocity.

Long press button_1 to change between A1, A2 and A3, A3 row.
Long press button_2 to change between play and edit modes.


Edit Mode:
knob_1: adjust pitch for current step & row
knob_2: adjust velocity for current step & row
button_1: trigger current step / toggle row
button_2: cycle to next step / change to Play mode
analog_1: pitch output
analog_2: velocity output
digital_1: step trigger

Play Mode:
knob_1: master tempo
button_1: play/pause
button_2: _ / change to Edit mode
analog_1: pitch output
analog_2: velocity output
digital_1: step trigger

"""
from machine import Pin
import uasyncio as asyncio
from utime import sleep_ms

# User libraries
from button import Pushbutton
from clock import Clock
from europi import *

DEBUG = True


# Create a full 3 octave chromatic scale for sequencer pitch.
chromatic_scale = create_scale(range(1,13), max_steps=37)


class Sequencer:
    # State variables
    run = False
    edit = True
    counter = 0
    row = 0
    _previous_pitch = 0
    _previous_velocity = 0
    
    # bit shift value for better analog precision
    _shift = 9
 
    def __init__(self, clock: Clock, seq_len: int = 8):
        # Initialize instance variables
        self.clock = clock
        self.seq_len = seq_len
        
        # Use digital led to show mode state.
        # Default state is edit mode with top row selected.
        digital_3.value(1)
        digital_4.value(0)
        
        # Set up the buttons
        Pushbutton(button_1.pin)\
            .press_func(self._short1)\
            .long_func(self._long1)

        Pushbutton(button_2.pin)\
            .press_func(self._short2)\
            .long_func(self._long2)

        self.pitch = [
            [0] * self.seq_len,
            [0] * self.seq_len,
        ]
        self.velocity = [
            [65535] * self.seq_len,
            [65535] * self.seq_len,
        ]
    
    def _short1(self):
        if self.edit:
            self.play_step()
        else:
            self.toggle_run()
    
    def _long1(self):
        if self.edit:
            self.toggle_row()
            
    def _short2(self):
        if self.edit:
            self.next_step()

    def _long2(self):
        self.toggle_edit()

    def toggle_run(self):
        """Toggle between sequence play/pause state."""
        self.run = not self.run
    
    def toggle_row(self):
        """Toggle between editing analogue rows."""
        self.row = (self.row + 1) % 2
        digital_3.value(1 if self.row == 0 else 0)
        digital_4.value(1 if self.row == 1 else 0)
    
    def toggle_edit(self):
        """Toggle between playback and edit mode."""
        if self.edit == True:
            self.edit = False
            self.run = True
            digital_2.value(0)
            digital_4.value(0)
            digital_3.value(0)
        else:
            self.edit = True
            self.run = False
            self.counter = 0
            digital_3.value(1 if self.row == 0 else 0)
            digital_4.value(1 if self.row == 1 else 0)

    def get_pitch(self):
        i = int((knob_1.percent() - 0.001) * len(chromatic_scale))
        return chromatic_scale[i]
    
    def get_velocity(self):
        # Bitshift from 16bit to 7 bit and back for less noise.
        return (knob_2.value() >> self._shift) << self._shift
    
    def adjust_step(self):
        # Adjust pitch
        pitch = self.get_pitch()
        if pitch != self._previous_pitch:
            self.pitch[self.row][self.counter] = pitch
            self._previous_pitch = pitch
        # Adjust velocity
        velocity = self.get_velocity()
        if velocity != self._previous_velocity:
            self.velocity[self.row][self.counter] = velocity
            self._previous_velocity = velocity
    
    def play_step(self):
        # Play pitch/velocity
        analogue_1.value(self.pitch[0][self.counter])
        analogue_2.value(self.velocity[0][self.counter])
        analogue_3.value(self.pitch[1][self.counter])
        analogue_4.value(self.velocity[1][self.counter])
        # Trigger digital 1
        digital_1.value(1); sleep_ms(10); digital_1.value(0)
        if DEBUG:
            print("S:{} R{} \tA1: {} \tA2: {} \tA3: {} \tA4: {}".format(
                self.counter, self.row,
                self.pitch[0][self.counter], self.velocity[0][self.counter],
                self.pitch[1][self.counter], self.velocity[1][self.counter]))

    def next_step(self):
        self.counter = (self.counter + 1) % self.seq_len
        # In edit mode blink d1 to show editing position.
        if self.edit:           
            if self.counter == 0:
                # Longer blink to indicate pattern start.
                digital_2.value(1); sleep_ms(500); digital_2.value(0)
            else:
                digital_2.value(1); sleep_ms(10); digital_2.value(0)

    async def start(self):
        while True:
            # Play sequence
            if self.run:
                self.clock.wait()
                self.play_step()
                self.next_step()

            # Edit sequence
            else:
                self.adjust_step()

            await asyncio.sleep_ms(10)


# Initialize a Clock for the sequencer.
# clock = Clock(clock_bus = Pin(4, Pin.IN), internal_clock = False)  # Use this with external clock source.
clock = Clock(knob_1)  # Use this clock config when no external EuroPi clock present.


# Initialize the sequence
seq = Sequencer(clock)


# Main script function
async def main():
    loop = asyncio.get_event_loop()
    loop.create_task(seq.start())
    loop.run_forever()


try:
    asyncio.run(main())
finally:
    asyncio.new_event_loop()


