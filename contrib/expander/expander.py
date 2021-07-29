from europi import AnalogueJack, DigitalJack, Button, UINT_16, create_scale
from machine import ADC, I2C, Pin, PWM
from ssd1306 import SSD1306_I2C
from time import sleep


class AnalogInput:
    def __init__(self, pin: Pin):
        self.pin = ADC(pin)
        self.scale = create_scale(range(1,13), 37)

    def value(self) -> int:
        """Read the received voltage as uint16 value between 0 and 65535."""
        return self.pin.read_u16()

    def percent(self) -> float:
        """Read the current relative voltage returned as a float between 0 and 1."""
        return self.pin.read_u16() / UINT_16


class DigitalInput:
    def __init__(self, pin):
        self.pin = pin

    def value(self):
        """Read the digital pin, HIGH (1) or LOW (0)."""
        self.pin.value()


# Joystick and button
class Joystick:
    def __init__(self):
        self._x = ADC(Pin(27))
        self._y = ADC(Pin(28))
        self._sw = Button(Pin(22,Pin.IN, Pin.PULL_UP))

    @property
    def x(self): 
        return self._x.read_u16()

    @property
    def y(self): 
        return self._y.read_u16()

    @property
    def sw(self): 
        return self._sw.value()
    
    def button_handler(self, func):
        self._sw.handler(func)


# Analog & Digital input jacks
analog_in = AnalogInput(Pin(26))
digital_in = DigitalInput(Pin(2, Pin.IN, Pin.PULL_DOWN))

# OLED display
i2c = I2C(0, sda=Pin(20), scl=Pin(21), freq=400000)
oled = SSD1306_I2C(128, 64, i2c)

# Joystick input
joystick = Joystick()

# Analog & Digital output jacks
analog_out = AnalogueJack(PWM(Pin(18, Pin.OUT)))
digital_out = DigitalJack(Pin(19, Pin.OUT))

