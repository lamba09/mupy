from machine import Pin
import time

relais = Pin(0, Pin.OUT)

while True:
    relais.value(not relais.value())
    time.sleep(1)