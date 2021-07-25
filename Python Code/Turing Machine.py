from europi import * #Required to be able to access the easy-use jacks, knobs, and buttons, without having to know the pin numbers

bounce_time = 0.5 #Minimum time between interrupts in seconds. If you having bouncing issues then increase this number
bouncer = 0 #Time since last interrupt

def int_handler_1(pin): #This controls what happens when the button 1 is pressed
    global bouncer #Gives access to the variable bouncer to allow it to see if it can be triggered again
    if bouncer > bounce_time: #Only if enough time has passed since last button press (set by bounce_time)
        button_1.irq(handler=None)
        print("Interrupt Detected!")
        global sequence #Gives access to the sequence so it can insert the new note
        sequence[note] = new_note #Inserts a new note the same way it would happen naturally
        digital_3.value(1) #Sets digital_3 high as this is the jack which indicates a new note has been created
        button_1.irq(handler=int_handler_1)
        bouncer = 0 #Reset the bouncer variable (the time since last interrupt)
button_1.irq(trigger=machine.Pin.IRQ_RISING, handler=int_handler_1) #Assign the interrupt function created above to button 1

def int_handler_2(pin): #The same button basics as for button 1
    global bouncer
    if bouncer > bounce_time:
        button_2.irq(handler=None)
        print("Interrupt Detected!")
        global lock #Gives access to the variable lock
        if lock == True: #Switches lock from either True to False or False to True
            lock = False
        else:
            lock = True
        button_2.irq(handler=int_handler_2)
        bouncer = 0 #Reset the bouncer variable (the time since last interrupt)
button_2.irq(trigger=machine.Pin.IRQ_RISING, handler=int_handler_2) #Assign the interrupt function created above to button 1

class TuringNote: #This object will contain the pins used for the note, and methods to allow the note to be played
    def __init__(self, clock, trigger_pin, gate_pin, pitch1_pin, pitch2_pin, timbre_pin): #The pins used by the note are passed in when it is created
        self.trigger_pin = trigger_pin
        self.gate_pin = gate_pin
        self.pitch1_pin = pitch1_pin
        self.pitch2_pin = pitch2_pin
        self.timbre_pin = timbre_pin
        
        #self.length = clock * choice([0.5, 1, 2, 4, 8])
        self.length = clock
        self.pitch_1 = choice(d_maj) #Change this scale to any of the available scales in the europi library or create your own (or set to randint(0,65535) to make it unquantised)
        self.pitch_2 = choice(d_maj) #Pitch 2 can be used for an alternating melody on a separate oscillator, but it's also useful as a general timbre control
        self.timbre = randint(0, 65535) #The timbre is fully randomised to get the full range
    
    def play(self): #A method to play the note using the jacks specified in the initialisation method
        self.pitch1_pin.value(self.pitch_1) #The pitch and timbre pins are all set first to avoid the short slew being heard
        self.pitch2_pin.value(self.pitch_2)
        self.timbre_pin.value(self.timbre)
        
        self.gate_pin.value(1) #The gate is turned on as this is 'open' the whole time the note is active
        
        self.trigger_pin.value(1) #The trigger pin is turned on
        sleep(0.05) #For 0.05seconds, within the Eurorack standard length
        self.trigger_pin.value(0) #The trigger pin is turned off
        
        sleep(abs(self.length - 0.05)) #The note 'sleeps' for its length minus the trigger time which has already happened
        global bouncer
        bouncer += abs(self.length - 0.05) #As the note slept for an amount of time, that time is added to the bouncer variable to tell the buttons they can be used again
        self.gate_pin.value(0) #Finally the gate is turned off again
        
        
sequence = [] #The sequence starts off as an empty array
sequence_length = 8 #You can change this length, 8 is standard
note = 0 #The index of the currently playing note in the sequence array
lock = False #A boolean that locks whether new notes can be created
while True: #The main program runs forever
    clock = (1 - (knob_1.percent() / 100)) + 0.01 #The clock calculation from knob 1. This gives you a time to sleep value between 0 seconds and 1 second. A very small value (0.01) is added to prevent it from breaking
    digital_4.value(0) #The sequence has started again, so the reset indicator is turned off
    
    new_note = TuringNote(clock, digital_1, digital_2, analogue_1, analogue_2, analogue_3) #A new note is created each time
    if len(sequence) == sequence_length: #The new note can only be swapped out if the sequence has reached its final length, so not for the first x steps
        if random_chance(knob_2.percent()): #The note is then dependent on the random chance controlled by knob 2
            if lock == False: #And finally, only if the new note creation is not locked according to button 2
                sequence[note] = new_note #If all these conditions are met, the note is added to the sequence at the current location
                digital_3.value(1) #The jack to indicate a new note has been added is turned on
    else:
        sequence.append(new_note) #If the sequence hasn't yet reached its full length, the note is added to the end
            
    analogue_4.value(randint(0,65535)) #The random CV is not tied to the notes, so is generated each time rather than within a note object
    sequence[note].play() #The current note is played
    digital_3.value(0) #The jack to indicate a new note is turned off as the note is over
    
    note += 1 #The index for sequence is incremented to move on to the next note
    if note == sequence_length: #If the note is at the end of the sequence
        note = 0 #It is reset to the start
        digital_4.value(1) #And the reset pin turned on to indicate this
        
    sleep(clock) #Finally, the time between notes is waited, as controlled by knob 1
    bouncer += clock #And as time has passed, that time is added to the bouncer variable for the button controls