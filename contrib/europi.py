"""
EuroPi Library
author: roryjamesallen
version: 1.1

EuroPi module library for pin wrappers and common utility functions.

https://github.com/roryjamesallen/EuroPi
https://allensynthesis.co.uk/europi_assembly.html
"""

from machine import Pin, PWM, ADC
from random import random, randint
from time import sleep, ticks_ms


####PINS####

knob_1 = ADC(Pin(28))
knob_2 = ADC(Pin(27))
button_1 = Pin(15, Pin.IN, Pin.PULL_UP)
button_2 = Pin(18, Pin.IN, Pin.PULL_UP)
digital_1 = Pin(21, Pin.OUT)
digital_2  = Pin(22, Pin.OUT)
digital_3  = Pin(19, Pin.OUT)
digital_4  = Pin(20, Pin.OUT)
analogue_1  = PWM(Pin(14, Pin.OUT))
analogue_2  = PWM(Pin(11, Pin.OUT))
analogue_3  = PWM(Pin(10, Pin.OUT))
analogue_4  = PWM(Pin(7, Pin.OUT))


####CLASSES####

class knob:
    def __init__(self, pin):
        self.pin = pin
        
    def percent(self):
        return int(self.pin.read_u16() / 655.35)
    
    def value(self):
        return(self.pin.read_u16())

class analogue_pin:
    def __init__(self, pin):
        self.pin = pin
        
    def value(self, new_duty):
        self.pin.duty_u16(new_duty)
        
    def randomise(self):
        self.duty(randint(0,65034))
        

class digital_pin:
    def __init__(self, pin):
        self.pin = pin
        
    def trigger(self):
        self.pin.value(1)
        sleep(0.05)
        self.pin.value(0)
        
    def value(self, value):
        self.pin.value(value)
        
    def toggle(self):
        self.pin.toggle()
        

####FUNCTIONS####        

def strum(trigger_pin, pitch_pin, count, time, notes):
    if len(notes) != count:
        print("Error: Please make sure you have a note pitch per pluck")
    else:
        for pluck in range(0,count-1):
            pitch_pin.value(notes[pluck])
            trigger_pin.value(1)
            sleep(time[0])
            trigger_pin.value(0)
            sleep(time[1])
            
            
def create_scale(notes):
    global chromatic_step
    scale = []
    pitch = 0
    step = 1
    while pitch < (chromatic_step * 37):
        if step in notes:
            scale.append(int(pitch))
        pitch += chromatic_step
        step += 1
        if step == 13:
            step = 1
    return scale

def random_chance(percentage):
    if randint(0,100) < percentage:
        return True
    else:
        return False
          
          
####VARIABLES####
    
chromatic_step = 65536 / (11.75 * 3.3)
            
c_maj = create_scale([1,3,5,6,8,10,12])
d_maj = create_scale([3,5,7,8,10,12])
d_min = create_scale([3,5,6,8,10,11])
jazz = create_scale([1,4,7,8,11])

d_maj_bass = d_maj[0:8]
d_min_bass = d_min[0:8]
c_maj_bass = c_maj[0:8]
jazz_bass = jazz[0:8]

analogue_1 = analogue_pin(analogue_1)
analogue_2 = analogue_pin(analogue_2)
analogue_3 = analogue_pin(analogue_3)
analogue_4 = analogue_pin(analogue_4)
digital_1 = digital_pin(digital_1)
digital_2 = digital_pin(digital_2)
digital_3 = digital_pin(digital_3)
digital_4 = digital_pin(digital_4)
knob_1 = knob(knob_1)
knob_2 = knob(knob_2)

if __name__ == "__main__":
    None
else:
    None







