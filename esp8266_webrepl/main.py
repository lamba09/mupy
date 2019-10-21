import time
from machine import Pin
led = Pin(2, Pin.OUT)  # turns on the LED

time.sleep(0.5)
led.on()
time.sleep(0.5)
led.off()

import wlan

time.sleep(0.5)
led.on()
time.sleep(0.5)
led.off()

import webrepl
webrepl.start()

time.sleep(0.5)
led.on()
