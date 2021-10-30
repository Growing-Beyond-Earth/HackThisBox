# GROWNG BEYOND EARTH CONTROL BOX
# RASPBERRY PI PICO / MICROPYTHON

# FAIRCHILD TROPICAL BOTANIC GARDEN, JULY 9, 2021

# The Growing Beyond Earth (GBE) control box is a device that controls
# the LED lights and fan in a GBE growth chamber. It can also control
# accessories including a 12v water pump and environmental sensors. 
# The device is based on a Raspberry Pi Pico microcontroller running 
# Micropython.

# This program Setup up the Time on the Hardware RTC and The Pico RTC 
#Written by MarioTheMaker 

import time
import ds3231
import machine
from machine import RTC
i2c0 = machine.I2C(0, sda=machine.Pin(16), scl=machine.Pin(17))

rtc=ds3231.DS3231(i2c0)

machine_rtc = RTC()
print(machine_rtc.datetime())
#rtc.datetime((2033, 8, 23, 2, 12, 48, 0, 0)) # set a specific date format
rtc.DateTime(machine_rtc.datetime()) 

#rtc.datetime() # get date and time
print (rtc.DateTime())


