from machine import Pin, PWM, ADC
from random import choice, randint
from time import sleep

EQUAL_TEMPERAMENT_VALUES = [17000, 19600, 22050, 24000, 25800, 27400, 28800, 30100, 31250, 32350, 33300, 34200, 35050, 35800, 36550, 37260, 37970, 38740, 39600]
C_MAJ = [17000, 22050, 27400, 28800]

knob_a = ADC(Pin(26))
knob_b = ADC(Pin(27))

digital_1 = Pin(0, Pin.OUT)
digital_2 = Pin(1, Pin.OUT)
digital_3 = Pin(2, Pin.OUT)
digital_4 = Pin(3, Pin.OUT)

digital_pins = [digital_1, digital_2, digital_3, digital_4]

analogue_1 = PWM(Pin(5, Pin.OUT))
analogue_2 = PWM(Pin(6, Pin.OUT))
analogue_3 = PWM(Pin(4, Pin.OUT))
analogue_4 = PWM(Pin(7, Pin.OUT))

analogue_pins = [analogue_1, analogue_2, analogue_3, analogue_4]

def trigger(pin): #A simple function to send a EuroRack 0.01 second trigger pulse to the assigned pin
    pin.value(1)
    sleep(0.01)
    pin.value(0)