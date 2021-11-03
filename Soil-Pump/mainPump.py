#====================================================================
#Main.py with example code for temp and moisture sensors and file data
#Mario The Maker & Eugene Francisco
#===================================================================

# GROWING BEYOND EARTH CONTROL BOX 
# RASPBERRY PI PICO / MICROPYTHON

# FAIRCHILD TROPICAL BOTANIC GARDEN, OCTOBER 20, 2021

# The Growing Beyond Earth (GBE) control box is a device that controls
# the LED lights and fan in a GBE growth chamber. It can also control
# accessories including a 12v water pump and environmental sensors. 
# The device is based on a Raspberry Pi Pico microcontroller running 
# Micropython.

# This program (main.py) runs automatically each time the device is
# powered up.



# ----------------SETTINGS FOR LIGHTS AND FAN-------------------

# LIGHTS -- Time values are hh:mm strings based on a 24h clock;  
#           brightness values are integers from 0 to 255 that set the
#           PWM duty cycle

#time values in file are in form [(year, month, day, mysteriousNumber, hour, minutes, seconds, mysteriousZero)]
lights_on_time = "13:15"
lights_off_time = "13:20"

red_brightness = 72
green_brightness = 60
blue_brightness = 44
white_brightness = 52


# FAN -- Fan power is an integer from 0 to 255 that sets the PWM
#        duty cycle

fan_power_when_lights_on = 255
fan_power_when_lights_off = 128

# --------------------------------------------------------------




# -----------------Load required libraries from /lib/-----------

from sys import stdin, stdout, exit
import machine
from machine import Pin, PWM, I2C
import utime, time
from time import sleep
from ds3231 import DS3231  # Hardware (I2C) real time clock
import ina219              # Current sensor
import ahtx0
from stemma_soil_sensor import StemmaSoilSensor

# ----------------Set up status LED on Control Box--------------
led = machine.PWM(machine.Pin(6))
led.freq(1000)
pump = Pin(7, Pin.OUT) #pump

# -------Set up I2C bus 0 for devices inside the control box---

i2c0 = machine.I2C(0, sda=machine.Pin(16), scl=machine.Pin(17))
ina = ina219.INA219(0.1,i2c0)   # Current sensor


# -------------Set up real time clock on I2C bus 0--------------
rtc = DS3231(i2c0) # Read Time from hardware RTC
rtc_time_tuple = rtc.DateTime() # Create a tuple with Time from Hardware RTC
rtci = machine.RTC()
rtci.datetime([x for x in rtc_time_tuple] + [0]) # Set local Machine time from Hardware RTC and add a 0 at the end. 
print(rtci.datetime())


# Translate the specified on/off times to seconds since midnight

onh, onm = map(int, lights_on_time.split(':')); on_seconds = (onh*60 + onm) * 60
offh, offm = map(int, lights_off_time.split(':')); off_seconds = (offh*60 + offm) * 60


# ---------------Set up LED and fan control--------------------
# Connect 24v MOSFETs to PWM channels on GPIO Pins 0-4
# Set PWM frequency on all channels

r=machine.PWM(machine.Pin(0)); r.freq(20000)   # Red channel
b=machine.PWM(machine.Pin(1)); b.freq(20000)   # Blue channel
g=machine.PWM(machine.Pin(2)); g.freq(20000)   # Green channel
w=machine.PWM(machine.Pin(3)); w.freq(20000)   # White channel
f=machine.PWM(machine.Pin(4)); f.freq(20000)   # Fan

# Clean up lights in case of a previous crash
r.duty_u16(0)
g.duty_u16(0)
b.duty_u16(0)
w.duty_u16(0)


# ----------------------Set up Functions -----------------------

def getRTC():
	# Attempt to read the time from the i2c real time clock and
	# catch any errors
	try:
	   rtc_dt=rtci.datetime()
	   print("Curent RTC",rtc_dt)
	   #Debug RTC
	except Exception as e:
	  print("An exception has occurred with the RTC: ", e)
	 
	rtc_seconds = ((((rtc_dt[4])*60) + rtc_dt[5]) * 60) + rtc_dt[6]
	#print("Seconds ",rtc_seconds) # Show Seconds 

	return rtc_dt, rtc_seconds

def controlLightsAndFan():
	if rtc_seconds >= on_seconds and rtc_seconds < off_seconds:
		# Lights on
		r.duty_u16(int(red_brightness)*256)
		g.duty_u16(int(green_brightness)*256)
		b.duty_u16(int(blue_brightness)*256)
		w.duty_u16(int(white_brightness)*256)
		f.duty_u16(fan_power_when_lights_on * 256)
	else:
		# Lights off
		r.duty_u16(int(red_brightness)*0)
		g.duty_u16(int(green_brightness)*0)
		b.duty_u16(int(blue_brightness)*0)
		w.duty_u16(int(white_brightness)*0)
		f.duty_u16(fan_power_when_lights_off * 256)

def pwmLED():
	try:
	   for duty in range(45000): led.duty_u16(duty); time.sleep(0.0001)
	   for duty in range(45000, 0, -1): led.duty_u16(duty); time.sleep(0.0001)
	

	except Exception as e:
	  print("An exception has occurred with the LED: ", e)
def currentSensor():     
	try:
	   ina.configure()
	   print("Voltage/current/power sensor readings:")
	   print("     Bus Voltage: %.3f V" % ina.voltage())
	   print("     Current: %.3f mA" % ina.current())
	   print("     Power: %.3f mW" % ina.power())
	
	except:
		print("Error reading from the current sensor", e)    
#===========================================================================================
#Example of Temp and Humid info, Eugene Francisco{
#===========================================================================================
def findTH(): #returns temperature in C and F and moisture
    try:
        # I2C for
        SDA_PIN = 18 # Define Pins
        SCL_PIN = 19 # Define Pins
        # Create the sensor object using I2C
        i2c = machine.I2C(1,sda=machine.Pin(SDA_PIN), scl=machine.Pin(SCL_PIN), freq=400000)
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
            
    except: #if doesn't work, returns error message and continues the program
        print("Error with current sensor", e) #"e" returns specific error message from program
        
def saveTimeTempHumid(time, tempC, tempF, humid):# saves all data in file
    file = open("Data.txt", "a")#creates file called "Data.txt" if it hasn't been created, or opens it if it has. "a" opens the file for appending
    file.write(str(time) + " " + str(tempC) + " " + str(tempF) + " " + str(humid)) #appends data in form (timeInfo, Ctemp, Ftemp, humidity)
    file.close()
   
    
#Debug Data File  
#    with open("Data.txt") as file: #opens Data.txt file to read
#        readData = file.read() #reads file data to "realData" 
#    print(readData)
#    file.close()

def pump_on(): #turn the pump on 
    pump.value(1)
    time.sleep(3) #how long should the pump run
    print("Pump On - Watering the Plant")
    
    
def pump_off(): #turn the pump off
    pump.value(0)
    print("Pump Off - Stop Watering the Plant")

def waterSystem():
    
    if findTH()[2] <400: #If he soil is less than 400 then turn the pump on 
      pump_on()
      pump_off()
    
    else:
        pump_off()

#===================================================================
#}
#===================================================================
# ----------------------------Main Start----------------------------
# Print information at startup
print("\nGROWING BEYOND EARTH, FAIRCHILD TROPICAL BOTANIC GARDEN\n")
print ("Software release date:\n 2021-11-03 experimental\n" )
print ("Internal clock time:")
print ("" + str(rtci.datetime()[0]) + "-" + str(rtci.datetime()[1]) + "-" + str(rtci.datetime()[2]) + "   " + str(rtci.datetime()[4]) + ":" + str(rtci.datetime()[5]) + ":" + str(rtci.datetime()[6]) + "\n") 
currentSensor()
#Main Loop    
while True:
	try:
		rtc_dt, rtc_seconds = getRTC()
		timeArr = [rtc_dt, rtc_seconds]
		controlLightsAndFan()
		pwmLED()
		#temp and moisture from sensor
		print("Temp C ", findTH()[0])
		print("Temp F ", findTH()[1])
		print("moisture ", findTH()[2])
		saveTimeTempHumid(timeArr, findTH()[0], findTH()[1], findTH()[2]) #saving to file Data.txt
		waterSystem()
		pwmLED()
		time.sleep(10) # Wait few seconds before repeating
		pwmLED()

	except Exception as e:
		print("failed Main Loop! Trying again: ", e)
