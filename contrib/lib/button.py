# Author: Kevin Köck
# Copyright Kevin Köck 2019-2020 Released under the MIT license
# Based on Peter Hinch's aswitch.py. Useable as a drop-in replacement.
# Queue overflow issue in Peter Hinch's aswitch fixed by now so this code
# only provides an alternative with less RAM usage.
# Created on 2019-10-19
# https://github.com/kevinkk525/pysmartnode/blob/master/pysmartnode/utils/abutton.py
#
# Updated 2021-09-04 by awonak
#  --removed double click functionality
#  --default to handle long press
#  --added more comments

__updated__ = "2021-09-04"
__version__ = "0.2"

import uasyncio as asyncio
import time

type_gen = type((lambda: (yield))())  # Generator type


# If a callback is passed, run it and return.
# If a coro is passed initiate it and return.
# coros are passed by name i.e. not using function call syntax.
def launch(func, tup_args):
    if func is None:
        return
    res = func(*tup_args)
    if isinstance(res, type_gen):
        loop = asyncio.get_event_loop()
        loop.create_task(res)


class Pushbutton:
    debounce_ms = 50
    long_press_ms = 1000

    _ta, _fa, _la = None, None, None

    def __init__(self, pin):
        self.pin = pin
        
        self._tf = None  # pressed function
        self._ff = None  # released function
        self._lf = None  # long pressed function
        
        self.sense = pin.value()  # Convert from electrical to logical value
        self.old_state = self.state  # Initial state
        
        loop = asyncio.get_event_loop()
        loop.create_task(self.buttoncheck())  # Thread runs forever

    def press_func(self, func, args=()):
        self._tf = func
        self._ta = args
        return self

    def release_func(self, func, args=()):
        self._ff = func
        self._fa = args
        return self

    def long_func(self, func, args=()):
        self._lf = func
        self._la = args
        return self

    # Current non-debounced logical button state: True == pressed
    @property
    def state(self):
        return bool(self.pin.value() ^ self.sense)

    async def buttoncheck(self):
        t_change = None
        longpress_ran = False

        # local functions for performance improvements
        deb = self.debounce_ms
        lpms = self.long_press_ms
        ticks_diff = time.ticks_diff
        ticks_ms = time.ticks_ms

        # Infinite async loop
        while True:
            cur_state = self.state
            # Conditional check for long press function.
            if cur_state is True and self.old_state is True:
                # Check if long press function should run.
                if longpress_ran is False:
                    if ticks_diff(ticks_ms(), t_change) >= lpms:
                        longpress_ran = True
                        launch(self._lf, self._la)
            # Button state has changed!
            elif cur_state != self.old_state:
                # Button pressed: launch pressed func.
                if cur_state is True:
                    launch(self._tf, self._ta)
                # Button released: launch release func.
                elif not longpress_ran:
                    launch(self._ff, self._fa)
                self.old_state = cur_state
                longpress_ran = False
                t_change = ticks_ms()
                
            # Ignore state changes until switch has settled
            await asyncio.sleep_ms(deb)
