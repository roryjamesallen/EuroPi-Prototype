from machine import Pin, UART
from ustruct import unpack
from utime import sleep_ms
from expander import display, digital_in, digital_out
from collections import namedtuple


uart1 = UART(1, baudrate=115200, tx=Pin(4), rx=Pin(5))
bus_clock = Pin(8, Pin.OUT)
led = Pin(25, Pin.OUT)


# Divisions state struct.
State = namedtuple("State", "selected_output d1 d2 d3 d4")
format_string = "5b"


def display_handler(state):  
    display.oled.fill(0)
    display.oled.text("Clock Divisions:", 0, 0)
    display.oled.text("D1: {}".format(state.d1), 0, 16)
    display.oled.text("D2: {}".format(state.d2), 64, 16)
    display.oled.text("D3: {}".format(state.d3), 0, 32)
    display.oled.text("D4: {}".format(state.d4), 64, 32)
    if state.selected_output != -1:
        msg = "selected: {}".format(state.selected_output + 1)
        display.oled.text(msg, 0, 48)
    display.oled.show()


def ready():
    led.off()
    display.oled.fill(0)
    # Flush the uart message buffer.
    for i in range(4):
        while uart1.any():
            print("init: {}".format(uart1.read()))
        sleep_ms(10)    


ready()
prev_digital = 0
while True:
    # Pass the input clock to EuroPi via bus clock.
    if digital_in.value() != prev_digital:
        bus_clock.toggle()
        digital_out.toggle()
        led.toggle()
        prev_digital = 1 if prev_digital == 0 else 0

    # Capture any UART messages and display if it's a division state message. 
    if uart1.any():
        try:
            state = State(*unpack(format_string, uart1.read()))
        except:
            # Ignore any uart message that is not a division state message.
            pass
        display_handler(state)
