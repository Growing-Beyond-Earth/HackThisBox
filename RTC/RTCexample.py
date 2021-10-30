import machine
from machine import RTC
rtc = machine.RTC()
print(rtc.datetime())
