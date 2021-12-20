#### NOTICE: This is a deprecated repository. It still contains accurate information for the original designs, however the new (much improved) version of the concept can now be found at the [EuroPi repository](https://github.com/Allen-Synthesis/EuroPi)
  
  
# EuroPi

The EuroPi is an open source project that integrates the new [Raspberry Pi Pico](https://www.raspberrypi.org/products/raspberry-pi-pico/) into a eurorack module.

All programs and code are available under the GNU General Public License v3.0. This is because I want all of my work to be available to anyone who would like to use it, modify it, and hopefully enjoy it. I have chosen this specific license because I want to ensure that this freedom of use will be granted to everyone in the future, and there is no risk of external profit motive reducing accessibility or driving up prices. 

Likewise, the hardware is all available under the Creative Commons Sharealike 4.0, which grants the same freedom in the hardware realm, so all of the PCB files, schematics, and anything else related to the hardware is in the public realm, but cannot be reproduced under a different license, so the idea cannot be bought up and then priced out of the pockets of many users.

# The EuroPi Library

The EuroPi library is regularly updated, and contains many functions and variables which will make using the EuroPi easier.

These include:
- Objects for each output jack, input button, and input knob
- Methods for each output jack to set its value intuitively (.value() for both digital and analogue, digital taking 0/1, and analogue taking 0-65535)
- Simple but useful functions for conversions, such as returning the knob value in a percentage form, allowing easy use for random chance.
