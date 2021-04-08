# EuroPi

The EuroPi is an open source project that integrates the new [Raspberry Pi Pico](https://www.raspberrypi.org/products/raspberry-pi-pico/) into a eurorack module. Further details can be found in the [wiki](https://github.com/roryjamesallen/EuroPi/wiki).


### Basic Functions

The Basic Functions code contains all of the header information you will need to use the EuroPi in its current setup. 
There are extended functions required for actually changing the values of the pins, which are included in the imported Pin and Machine libraries.
For example, to change an analogue pin's value, the method is .duty_u16(), which is a bit confusing, so I'm planning to make some more simple functions like trigger() to allow them to be used more intuitively.
