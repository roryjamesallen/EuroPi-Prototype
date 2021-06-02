from machine import Pin, PWM, ADC
from random import choice, randint
from time import sleep


####PINS####
#Don't change these values unless you are modifying the hardware, as the pins connected to the Pico are preset by the PCB layout.
knob_2 = ADC(Pin(27))
knob_1 = ADC(Pin(28))
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
        
    def percent(self):  #This allows a knob to be read as a percentage, which makes it much easier to use for random chance.
        return int(self.pin.read_u16() / 655.35)
    

class analogue_pin:
    def __init__(self, pin):
        self.pin = pin
        
    def value(self, new_duty):  #Accepts 0-65535
        self.pin.duty_u16(new_duty)
        
    def randomise(self):    #Assigns the value automatically to a random voltage
        self.duty(randint(0,65034))
        

class digital_pin:
    def __init__(self, pin):
        self.pin = pin
        
    def trigger(self):  #Sends a EuroRack standard trigger. Not usable if you're triggering multiple pins simultaneously
        self.pin.value(1)
        sleep(0.05)
        self.pin.value(0)
        
    def value(self, value): #Accepts 0-1, off/on
        self.pin.value(value)
        
    def toggle(self):   #Toggles the value, helpful if the current value isn't known/required
        self.pin.toggle()
      
    
####FUNCTIONS####      
def create_scale(notes):    #Creates a chromatic scale based on the given positions of notes within a chromatic octave. Positions start at 1 for ease of use
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

def random_chance(percentage):  #Calculates a boolean output based on a given percentage chance of being True
    if randint(0,100) < percentage:
        return True
    else:
        return False
          
          
####VARIABLES####
chromatic_step = 65536 / (11.75 * 3.3)  #Don't change this unless you are having 1V/Oct tracking issues. The method used for converting digital to analogue is imperfect, so the value of 11.75 is carefully calculated to account
            
####SCALES####
#To create a scale, simply use the create_scale function, passing in an array with the position of the notes in the scale.
#For example, a c_maj scale is formed of the 1st, 3rd, 5th, 6th, 8th, 10th, and 12th notes of a chromatic octave. 
c_maj = create_scale([1,3,5,6,8,10,12])
d_maj = create_scale([3,5,7,8,10,12])
d_min = create_scale([3,5,6,8,10,11])
jazz = create_scale([1,4,7,8,11])

#Bass scales, often useful if you want a smaller range of a scale
d_maj_bass = d_maj[0:8]
d_min_bass = d_min[0:8]
c_maj_bass = c_maj[0:8]
jazz_bass = jazz[0:8]

#Re-define the pins as objects, allowing their new methods to be accessed
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

#Ignore this section as this module is always imported rather than run itself
if __name__ == "__main__":
    None
else:
    None






