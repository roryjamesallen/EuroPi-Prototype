from machine import Pin
from expander import UINT_16, analog_in, digital_in, analog_out, digital_out, joystick, oled
from europi import c_maj
from time import sleep


led = Pin(25, Pin.OUT)
read_d = 0

counter = 0
while True:
    msg = ""
    # Analog in
    read_a = analog_in.value()
    analog_msg = "Analog: {}".format(read_a)


    # Digital in
    if digital_in.value() != read_d:
        read_d = digital_in.value()
        led.toggle()
    digital_msg = "Digital: {}".format(read_d)


    # Joystick
    joystick_msg = "X: " + str(joystick.x)
    joystick_msg2 = "Y: " + str(joystick.y)
    joystick_msg3 = "SW: " + str(joystick.sw)


    # Analog out
    analog_out.value(c_maj[counter])
    counter += 1
    if counter == len(c_maj):
        counter = 0


    # Digital out
    digital_out.trigger()


    # OLED
    oled.fill(0)
    oled.text(analog_msg, 0, 0)
    oled.text(digital_msg, 0, 12)
    oled.text(joystick_msg, 0, 24)
    oled.text(joystick_msg2, 0, 36)
    oled.text(joystick_msg3, 0, 48)
    oled.show()


    sleep(0.2)

