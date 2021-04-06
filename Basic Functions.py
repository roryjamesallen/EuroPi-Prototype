from machine import Pin, PWM, ADC
from random import choice, randint
from time import sleep

EQUAL_TEMPERAMENT_VALUES = [
    17000,
    19600,
    22050,
    24000,
    25800,
    27400,
    28800,
    30100,
    31250,
    32350,
    33300,
    34200,
    35050,
    35800,
    36550,
    37260,
    37970,
    38740,
    39600,
]
C_MAJ = [17000, 22050, 27400, 28800]

k1 = ADC(
    Pin(28)
)  # Assigns the GPIO pins that are related to the two knobs on the board, and sets them up as ADC channels
k2 = ADC(Pin(27))

b1 = Pin(
    15, Pin.IN, Pin.PULL_UP
)  # Assigns the GPIO pins for the two buttons on the board. The board does not contain pull up resistors, as they can be programmed here (the Pico has inbuilt software pull up resistors)
b2 = Pin(18, Pin.IN, Pin.PULL_UP)

dj1 = Pin(
    21, Pin.OUT
)  # Assigns the 4 digital pins to the GPIOs they are related to. These pins can be found in the 'Pin Values' file on GitHub, and the 'djx' terms match with the PCB labeling
dj2 = Pin(22, Pin.OUT)
dj3 = Pin(19, Pin.OUT)
dj4 = Pin(20, Pin.OUT)

digital_pins = [
    dj1,
    dj2,
    dj3,
    dj4,
]  # Creates an array so that the digital pins can be iterated through (allows them to all work in unison/related to each other)

aj1 = PWM(
    Pin(14, Pin.OUT)
)  # Assigns the 4 analogue pins to the GPIOs they are related to. These pins can be found in the 'Pin Values' file on GitHub, and the 'ajx' terms match with the PCB labeling
aj2 = PWM(Pin(11, Pin.OUT))
aj3 = PWM(Pin(10, Pin.OUT))
aj4 = PWM(Pin(7, Pin.OUT))

analogue_pins = [
    aj1,
    aj2,
    aj3,
    aj4,
]  # Creates an array so that the analogue pins can be iterated through (allows them to all work in unison/related to each other)


def trigger(
    pin,
):  # A simple function to send a EuroRack 0.01 second trigger pulse to the assigned pin
    pin.value(1)
    sleep(0.01)
    pin.value(0)


def gate(
    pin, time
):  # A function to send a gate output via a digital pin for a specified gate time
    pin.value(1)
    sleep(time)
    pin.value(0)


def attack_release(
    pin, attack, release
):  # A function to send an attack release pulse on an analogue pin, rising and falling over the specified time.
    attack_step = (
        attack / 100
    )  # It only divides the steps into 100, so if the attack or release is especially long you might need to increase this
    value = 0
    for step in range(0, 99):  # Increase over 100 steps
        pin.u_duty16(value)
        sleep(attack_step)
        value += (
            65025 / 100
        )  # Adding the maximum value/100 each step (after 100 it reaches the maxiumum)

    release_step = release / 100  # Does the exact same but for release
    value = 0
    for step in range(0, 99):
        pin.u_duty16(value)
        sleep(release_step)
        value -= 65025 / 100  # Subtracts the value instead of adding

