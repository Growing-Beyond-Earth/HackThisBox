from machine import Pin, Timer
led = Pin(6, Pin.OUT)
timer = Timer()

def blink(timer):
    led.toggle()

timer.init(freq=.5, mode=Timer.PERIODIC, callback=blink)