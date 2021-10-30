import utime
from machine import Pin, I2C

import ahtx0

# I2C for
i2c = I2C(1,scl=Pin(19), sda=Pin(18))

# Create the sensor object using I2C
sensor = ahtx0.AHT10(i2c)

Ctemp=sensor.temperature
Ftemp=(Ctemp*1.8+32)
humidity=sensor.relative_humidity

while True:
    print("\nTemperature: %0.2f C" % Ctemp)
    print("Temperature: %0.2f F" % Ftemp)
    print("Humidity: %0.2f %%" % humidity)
    utime.sleep(5)

