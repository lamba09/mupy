# main.py -- put your code here!
import time
from pyb import UART
from pyb import LED
from pyb import Pin

StartStopLED = Pin('Y10', Pin.OUT_PP)
GreenLED = Pin('Y11', Pin.OUT_PP)
RedLED = Pin('Y12', Pin.OUT_PP)

StartButton = Pin('X1', Pin.IN)
StopButton = Pin('X2', Pin.IN)
GreenButton = Pin('X3', Pin.IN)
BlackButton = Pin('X4', Pin.IN)
Switch = Pin('X5', Pin.IN)
RemoteTrigger = Pin('X6', Pin.IN, Pin.PULL_UP)


def is_pressed(button):
    return button.value() == 0


def printing_active():
    active = time.time() < last_print_time + 55
    RedLED.value(active)
    return active

def test_image_enabled():
    return is_pressed(Switch)

def cancel_current_print():
    time.sleep(0.5)
    cancel_print()
    time.sleep(0.5)
    cancel_print()
    time.sleep(0.5)
    cancel_print()

last_print_time = time.time() - 100

def handle_printing():
    global last_print_time
    if printing_active() and test_image_enabled():
        cancel_current_print()
        time.sleep(5)
        return
    if not printing_active():
        last_print_time = time.time()
    if test_image_enabled():
        time.sleep(5)
        return
    while printing_active():
        time.sleep(0.1)

RED = LED(1)
GREEN = LED(2)
YELLOW = LED(3)
BLUE = LED(4)

uart = UART(1, 38400)

# CONFIG  = b'\x0e$\x00\x10\x00\x13\x88\x00\x00\x00\x00\x00\\\x84 '
CONFIG = b'\x06$\x00\x10\x00\x4e\x08\x00\x00\x00\x00\x00\xab\x68 '

def trigger():
    uart.write(b'\x02t ')

def cancel_print():
    uart.write(b'\x02c ')

def connect():
    uart.write(b'b')

def ack():
    uart.write(b'\x02k ')

BLUE.on()
RedLED.high()

# wait for ready software
while True:
    if uart.any():
        data = uart.read()
        if b'\x02i ' in data:
            connect()
            break
    # if is_pressed(RemoteTrigger):
    #     break
    time.sleep(0.2)

BLUE.off()
YELLOW.on()
GreenLED.high()

# configure
while True:
    if uart.any():
        data = uart.read()
        if b'\x02? ' in data:
            uart.write(CONFIG)
            break
    # if is_pressed(RemoteTrigger):
    #     break
    time.sleep(0.2)

YELLOW.off()
RED.on()
RedLED.low()

# ackknowledge config
while True:
    if uart.any() >= 64:
        data = uart.read(64)
        if CONFIG in data:
            ack()
            break
    # if is_pressed(RemoteTrigger):
    #     break
    time.sleep(0.2)

RED.off()
GreenLED.low()

time.sleep(1)

while True:
    GreenLED.high()
    if is_pressed(RemoteTrigger):
        trigger()
        GreenLED.low()
        handle_printing()
    while printing_active() and not test_image_enabled():
        GreenLED.low()
        time.sleep(0.1)
    time.sleep(0.05)
