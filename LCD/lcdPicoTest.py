#lcdPicoTest.py
#Written by @Mario The Maker 

from machine import I2C, Pin
from time import sleep
from pico_i2c_lcd import I2cLcd
i2c = I2C(1, sda=Pin(26), scl=Pin(27), freq=400000)
#i2c = machine.I2C(1, sda=machine.Pin(30), scl=machine.Pin(31), freq=400000)

I2C_ADDR = i2c.scan()[0]
lcd = I2cLcd(i2c, I2C_ADDR, 2, 16)
while True:
    print(I2C_ADDR)
    lcd.blink_cursor_on()
   
    lcd.putstr("I2C Address:"+str(I2C_ADDR)+"\n")
    lcd.putstr("LCD Test")
    sleep(2)
    lcd.clear()
    lcd.putstr("I2C Address:"+str(hex(I2C_ADDR))+"\n")
    sleep(2)
    lcd.blink_cursor_off()
    lcd.clear()
    lcd.putstr("Backlight Test")
    for i in range(10):
        lcd.backlight_on()
        sleep(0.2)
        lcd.backlight_off()
        sleep(0.2)
    lcd.backlight_on()
    lcd.hide_cursor()
    for i in range(20):
        lcd.putstr(str(i))
        sleep(0.4)
        lcd.clear()
