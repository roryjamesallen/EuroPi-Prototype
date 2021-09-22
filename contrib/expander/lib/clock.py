"""
Clock
author: awonak
version: 1.0

Provide a master clock tempo from internal or external source.

This library provides scripts with a set of functions for providing an internal
clock set by a knob that includes average run smoothing to account for analog
fluxuation. Additionally, read a GPIO pin from the Expander module to use a
clock from an external source.


knob_1: internal master clock tempo
button_1: switch between internal or external clock source.


Expander:

# Digital pin to read input clock from the expander.
Pin(8): cv clock output

"""
from machine import Pin
from utime import sleep


class Clock:
    """Define a master clock either using internal or external source."""
    
    def __init__(self, tempo_knob: Pin, clock_switch: Pin, external_clock: Pin,
                 min_bpm: int = 20, max_bpm: int = 280) -> None:
        self._internal_clock = True

        # Input controls for internal clock.
        self.tempo_knob = tempo_knob
        clock_switch.handler(self.switch_clock_source)

        # GPIO Pin with external clock source.
        self.external_clock = external_clock
        self._prev_clock = 0

        # Tempo range vars
        self.min_bpm = min_bpm
        self.max_bpm = max_bpm
        self.tempo = 0

        # Running average vars for smoothing analog input for tempo.
        self._run_len = 10
        self._run = [self.get_internal_tempo()] * self._run_len

    def switch_clock_source(self) -> None:
        """Switch between internal and external clock source."""
        self._internal_clock = not self._internal_clock
    
    def get_internal_tempo(self) -> float:
        """Take a reading from the tempo knob to determine internal tempo."""
        # Set the clock speed via Knob 1.
        # tempo range default is between 20 and 280 BPM.
        # Knob 12 o'clock position is 150 BPM.
        return (self.tempo_knob.percent() * (self.max_bpm - self.min_bpm)) + self.min_bpm

    def internal_clock_wait(self) -> None:
        """Wait for a quarter note of the internal tempo."""
        # Get the running average tempo.
        self._run = self._run[1:]
        self._run.append(self.get_internal_tempo())
        self.tempo = round(sum(self._run) / self._run_len, 1)
        # Sleep for a quarter note of the tempo.
        sleep((60 / self.get_internal_tempo()) / 4)
    
    def external_clock_wait(self) -> None:
        """Wait for clock pulse to go high to advance."""
        while not self._internal_clock:
            if self.external_clock.value() != self._prev_clock:
                self._prev_clock = 1 if self._prev_clock == 0 else 0
                if self._prev_clock == 0:
                    return

    def wait(self) -> None:
        """Wait for a clock cycle of the current selected clock source."""
        if self._internal_clock:
            self.internal_clock_wait()
        else:
            self.external_clock_wait()
