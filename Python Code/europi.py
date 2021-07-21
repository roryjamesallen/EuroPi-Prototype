"""
EuroPi Library
author: roryjamesallen
version: 1.1

EuroPi module library for pin wrappers and common utility functions.
https://github.com/roryjamesallen/EuroPi
https://allensynthesis.co.uk/europi_assembly.html
"""

from machine import Pin, PWM, ADC
from random import choice, random
from time import sleep, ticks_ms


UINT_16 = 65535  # Maximum unsigned 16 bit integer value.
MAX_DUTY = 65025  # Max u16 value with offset.

####PINS####

knob_1 = ADC(Pin(28))
knob_2 = ADC(Pin(27))
button_1 = Pin(15, Pin.IN, Pin.PULL_UP)
button_2 = Pin(18, Pin.IN, Pin.PULL_UP)
digital_1 = Pin(21, Pin.OUT)
digital_2 = Pin(22, Pin.OUT)
digital_3 = Pin(19, Pin.OUT)
digital_4 = Pin(20, Pin.OUT)
analogue_1 = PWM(Pin(14, Pin.OUT))
analogue_2 = PWM(Pin(11, Pin.OUT))
analogue_3 = PWM(Pin(10, Pin.OUT))
analogue_4 = PWM(Pin(7, Pin.OUT))


####CLASSES####


class Knob:
    def __init__(self, pin):
        self.pin = pin

    # Provide the relative percent value between 0 and 1.
    def percent(self):
        return self.value() / UINT_16

    # Provide the current value of the knob position between 0 and 65535 (max 16 bit int).
    def value(self):
        return self.pin.read_u16()


class Button:
    def __init__(self, pin, debounce_delay=500):
        self.pin = pin
        self.debounce_delay = debounce_delay
        self.last_pressed = 0
        self.debounce_done = True

    def _debounce_check(self):
        if (ticks_ms() - self.last_pressed) > self.debounce_delay:
            self.debounce_done = True

    # Handler takes a callback func to call when this button is pressed.
    def handler(self, func):
        def bounce(func):
            def wrap_bounce(*args, **kwargs):
                self._debounce_check()
                if self.debounce_done:
                    self.last_pressed = ticks_ms()
                    self.debounce_done = False
                    func()

            return wrap_bounce

        self.pin.irq(trigger=Pin.IRQ_RISING, handler=bounce(func))


class AnalogueJack:
    def __init__(self, pin):
        self.pin = pin

    # Set the duty value to the given unsigned 16 bit int value.
    def value(self, new_duty):
        self.pin.duty_u16(new_duty)

    # Calling randomise will set the duty to a random value within the acceptable range.
    def randomise(self):
        self.duty(randint(0, MAX_DUTY))


class DigitalJack:
    def __init__(self, pin):
        self.pin = pin

    # Set the digital pin to the given value, HIGH (1) or LOW (0).
    def value(self, value):
        self.pin.value(value)

    # Set the digital pin to HIGH for the optional duration (default to 50ms).
    def trigger(self, sleep_duration=0.05):
        self.value(1)
        sleep(sleep_duration)
        self.value(0)

    # Invert the digital pin's current value.
    def toggle(self):
        self.pin.toggle()


####FUNCTIONS####


def strum(trigger_pin, pitch_pin, count, time, notes):
    if len(notes) != count:
        print("Error: Please make sure you have a note pitch per pluck")
    else:
        for pluck in range(0, count - 1):
            pitch_pin.value(notes[pluck])
            trigger_pin.trigger(time[0])
            sleep(time[1])


def create_scale(notes):
    global chromatic_step
    scale = []
    note = 0
    step = 1
    while note < (chromatic_step * 36):
        if step in notes:
            scale.append(int(note))
        note += chromatic_step
        step += 1
        if step == 13:
            step = 1
    return scale


def random_chance(percentage):
    return random() < percentage


####VARIABLES####

chromatic_step = UINT_16 / (11.75 * 3.3)

c_maj = create_scale([1, 3, 5, 6, 8, 10, 12])
d_maj = create_scale([3, 5, 7, 8, 10, 12])
d_min = create_scale([3, 5, 6, 8, 10, 11])
jazz = create_scale([1, 4, 7, 8, 11])

d_maj_bass = d_maj[0:8]
d_min_bass = d_min[0:8]
c_maj_bass = c_maj[0:8]
jazz_bass = jazz[0:8]

analogue_1 = AnalogueJack(analogue_1)
analogue_2 = AnalogueJack(analogue_2)
analogue_3 = AnalogueJack(analogue_3)
analogue_4 = AnalogueJack(analogue_4)
digital_1 = DigitalJack(digital_1)
digital_2 = DigitalJack(digital_2)
digital_3 = DigitalJack(digital_3)
digital_4 = DigitalJack(digital_4)
knob_1 = Knob(knob_1)
knob_2 = Knob(knob_2)
button_1 = Button(button_1)
button_2 = Button(button_2)
