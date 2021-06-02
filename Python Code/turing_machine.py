from europi import *


class TuringNote:
    def __init__(self, clock, trigger_pin, gate_pin, pitch1_pin, pitch2_pin, timbre_pin):
        self.trigger_pin = trigger_pin
        self.gate_pin = gate_pin
        self.pitch1_pin = pitch1_pin
        self.pitch2_pin = pitch2_pin
        self.timbre_pin = timbre_pin
        
        self.length = clock
        self.pitch_1 = choice(d_maj)
        self.pitch_2 = choice(d_maj)
        self.timbre = randint(0, 65535)
    
    def play(self):
        self.pitch1_pin.value(self.pitch_1)
        self.pitch2_pin.value(self.pitch_2)
        self.timbre_pin.value(self.timbre)
        
        self.gate_pin.value(1)
        
        self.trigger_pin.value(1)
        print("play note")
        sleep(0.05)
        self.trigger_pin.value(0)
        
        sleep(abs(self.length - 0.05))
        self.gate_pin.value(0)
        
class Rest:
    def __init__(self, length):
        self.length = length
        
    def play(self):
        print("play rest")
        sleep(self.length)
        
        
sequence = []
sequence_length = 16
note = 0
while True:
    clock = (1 - (knob_1.percent() / 100))
    
    if randint(0,10) < 3:
        new_note = Rest(clock)
    else:   
        new_note = TuringNote(clock, digital_1, digital_2, analogue_1, analogue_2, analogue_3)
    
    if len(sequence) == sequence_length:
        if random_chance(knob_2.percent()):
            sequence[note] = new_note
    else:
        sequence.append(new_note)
            
    analogue_4.value(randint(0,65535))
    sequence[note].play()
    
    note += 1
    if note == sequence_length:
        note = 0
        
    sleep(clock)

