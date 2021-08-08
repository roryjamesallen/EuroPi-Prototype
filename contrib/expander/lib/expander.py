from europi import AnalogueJack, DigitalJack, Button, UINT_16
from machine import ADC, I2C, Pin, PWM
from ssd1306 import SSD1306_I2C


# OLED size constants
WIDTH = 128
HEIGHT = 64


class AnalogInput:
    def __init__(self, pin: Pin):
        self.pin = ADC(pin)

    def value(self) -> int:
        """Read the received voltage as uint16 value between 0 and 65535."""
        return self.pin.read_u16()

    def percent(self) -> float:
        """Read the current relative voltage returned as a float between 0 and 1."""
        return self.pin.read_u16() / UINT_16


class DigitalInput:
    def __init__(self, pin: Pin):
        self.pin = pin

    def value(self) -> int:
        """Read the digital pin, HIGH (1) or LOW (0)."""
        return self.pin.value()


# OLED Display
class Display:
    def __init__(self, sda: Pin, scl: Pin, freq: int = 400000):
        self.i2c = I2C(0, sda=sda, scl=scl, freq=freq)
        if len(self.i2c.scan()) == 0:
            print("No I2C devices found!")
            return

        self.oled = SSD1306_I2C(WIDTH, HEIGHT, self.i2c)


# Joystick and button
class Joystick:
    def __init__(self, pin_x: Pin, pin_y: Pin, pin_button: Pin):
        self._x = ADC(pin_x)
        self._y = ADC(pin_y)
        self._sw = Button(pin_button)

    @property
    def x(self) -> int: 
        return self._x.read_u16()

    @property
    def y(self) -> int: 
        return self._y.read_u16()
    
    def button_handler(self, func):
        self._sw.handler(func)


# Analog & Digital input jacks
analog_in = AnalogInput(Pin(26))
digital_in = DigitalInput(Pin(2, Pin.IN, Pin.PULL_DOWN))

# OLED display
display = Display(Pin(20), Pin(21))

# Joystick input
joystick = Joystick(Pin(27), Pin(28), Pin(22, Pin.IN, Pin.PULL_UP))

# Analog & Digital output jacks
analog_out = AnalogueJack(PWM(Pin(18, Pin.OUT)))
digital_out = DigitalJack(Pin(19, Pin.OUT))
