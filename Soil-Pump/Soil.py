import utime
from machine import Pin, I2C

from stemma_soil_sensor import StemmaSoilSensor

SDA_PIN = 18 # update this
SCL_PIN = 19 # update this

#i2c0 = machine.I2C(0, sda=machine.Pin(16), scl=machine.Pin(17))

i2c = machine.I2C(1,sda=machine.Pin(SDA_PIN), scl=machine.Pin(SCL_PIN), freq=400000)
seesaw = StemmaSoilSensor(i2c)

# get moisture
moisture = seesaw.get_moisture()

# get temperature
temperature = seesaw.get_temp()
ftemperature=(temperature*1.8+32)

print("\nTemperature: %0.2f C" % temperature)
print("Temperature: %0.2f F" % ftemperature)
print("Moisture: %0.2f " % moisture)
