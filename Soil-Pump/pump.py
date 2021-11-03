# Connect 12v MOSFET to GPIO Pin 7 for on/off control of water pump
# Mario The Maker 

from machine import Pin, I2C
import time
import utime
from stemma_soil_sensor import StemmaSoilSensor

#Define Pins and i2c
pump = Pin(7, Pin.OUT) #pump
SDA_PIN = 18 # Define Pins
SCL_PIN = 19 # Define Pins
i2c = machine.I2C(1,sda=machine.Pin(SDA_PIN), scl=machine.Pin(SCL_PIN), freq=400000)

#------------ Functions ------------------------

def pump_on(): #turn the pump on 
    pump.value(1)
    time.sleep(5) #how long should the pump run
    print("Pump On - Watering the Plant")
    
    
def pump_off(): #turn the pump off
    pump.value(0)
    print("Pump Off - Stop Watering the Plant")


def GetSensor(): #get all the sensor data  
    seesaw = StemmaSoilSensor(i2c)
    # get moisture
    moisture = seesaw.get_moisture()
    # get temperature
    temperature = seesaw.get_temp()
    ftemperature=(temperature*1.8+32)
    dataArr = [0,0,0] #array to save temp in celsius, farenheight, and humidity
    dataArr[0] = temperature #first element of arr is C
    dataArr[1] = ftemperature #second element of arr is F
    dataArr[2] = moisture #third element of arr is humidity
    return dataArr #returns list in form [Ctemp, Ftemp, humidity]
   
#------------ Main ------------------------    

while True:
    print("Temp C ", GetSensor()[0])
    print("Temp F ", GetSensor()[1])
    print("moisture ", GetSensor()[2])
    if GetSensor()[2] <400: #If he soil is less than 400 then turn the pump on 
       pump_on()
       pump_off()
    else:
        pump_off()
    time.sleep(2)   
