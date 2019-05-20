from machine import Pin, I2C
import time
import servo

WIDTH = 64
HEIGHT = 48
ADDRESS = 0x40

i2c = I2C(scl=Pin(5), sda=Pin(4), freq=100000)

s = servo.Servo(i2c)

def swipe(delay):
    deg = 0
    d = 1
    while True:
        if deg > 120:
            d = -1
        if deg < 0:
            d = 1
        deg += d
        s.position(0, degrees=deg)
        time.sleep(delay)
