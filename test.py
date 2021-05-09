from machine import Pin, PWM, ADC
from random import choice, randint
from time import sleep

#Assign each of the inputs and outputs on the front board to the relevant GPIO pins of the Pico
knob_1 = ADC(Pin(28))
knob_2 = ADC(Pin(27))
button_1 = Pin(15, Pin.IN, Pin.PULL_UP)
button_2 = Pin(18, Pin.IN, Pin.PULL_UP)
digital_1 = Pin(21, Pin.OUT)
digital_2  = Pin(22, Pin.OUT)
digital_3  = Pin(19, Pin.OUT)
digital_4  = Pin(20, Pin.OUT)
analogue_2  = PWM(Pin(14, Pin.OUT))
analogue_1  = PWM(Pin(11, Pin.OUT))
analogue_4  = PWM(Pin(10, Pin.OUT))
analogue_3  = PWM(Pin(7, Pin.OUT))

digital_pins = [digital_1, digital_2, digital_3, digital_4]
digital_pin = digital_pins[0]

#Set up some variables that are used to allow button 1 to interrupt the program
#The bounce variables are to prevent "bouncing" where the button triggers the interrupt multiple times per press
on = 1
bounce_time = 0.2 #Minimum time between interrupts in seconds. If you having bouncing issues then increase this number
bouncer = 0 #Time since last interrupt

def trigger(pin):
    pin.toggle()
    sleep(0.1)
    pin.toggle()

#Set up the interrupt function to allow the button to interrupt the program
def int_handler_1(pin):
    global bouncer
    if bouncer > bounce_time:
        button_1.irq(handler=None)
        print("Interrupt Detected!")
        global digital_pin
        digital_pin.toggle()
        button_1.irq(handler=int_handler_1)
        bouncer = 0 #Reset the bouncer variable (the time since last interrupt)
        
def int_handler_2(pin):
    global bouncer
    if bouncer > bounce_time:
        button_2.irq(handler=None)
        print("Interrupt Detected!")
        global digital_pins
        global digital_pin
        try:
            #digital_pin.value(0)
            digital_pin = digital_pins[digital_pins.index(digital_pin) + 1]
            trigger(digital_pin)
        except:
            digital_pin = digital_pins[0]
            trigger(digital_pin)
        button_2.irq(handler=int_handler_2)
        bouncer = 0 #Reset the bouncer variable (the time since last interrupt)


button_1.irq(trigger=machine.Pin.IRQ_RISING, handler=int_handler_1) #Assign the interrupt function created above to button 1
button_2.irq(trigger=machine.Pin.IRQ_RISING, handler=int_handler_2) #Assign the interrupt function created above to button 1

while True: #The program will run forever
    sleep(0.01) #The remaining clock time (minus the time already waited while on) is "slept" for
    bouncer += (0.01) #The time since last interrupt is incremented by the total time waited, 1/8 (clock) seconds.



