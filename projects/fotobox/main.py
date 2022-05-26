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


def cancel_request():
    cancel_buttons = map(is_pressed, [RemoteTrigger, StopButton, BlackButton, GreenButton])
    if any(cancel_buttons):
        return True
    return False


def handle_printing():
    time.sleep(0.5)
    if not is_pressed(Switch):
        cancel_print()
        time.sleep(0.5)
        cancel_print()
        time.sleep(0.5)
        cancel_print()
    else:
        RedLED.high()
        cancelled = False
        for i in range(50):
            if cancel_request():
                cancel_print()
                time.sleep(0.2)
                cancel_print()
                cancelled = True
                break
            time.sleep(0.1)
        if not cancelled:
            time.sleep(50)
        RedLED.low()
    time.sleep(5)


def timer(seconds):
    timer_cancelled = False
    for i in range(1, 10*int(seconds)+1):
        if is_pressed(StopButton):
            timer_cancelled = True
            break
        time.sleep(0.1)
        if i % 10 == 0:
            StartStopLED.high()
        elif (i + 3) % 10 == 0:
            StartStopLED.low()
    if not timer_cancelled:
        trigger()
        handle_printing()
    StartStopLED.low()

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

while True:
    if uart.any():
        data = uart.read()
        if b'\x02i ' in data:
            connect()
            break
    if is_pressed(RemoteTrigger):
        break
    time.sleep(0.2)

BLUE.off()
YELLOW.on()
GreenLED.high()

while True:
    if uart.any():
        data = uart.read()
        if b'\x02? ' in data:
            uart.write(CONFIG)
            break
    if is_pressed(RemoteTrigger):
        break
    time.sleep(0.2)

YELLOW.off()
RED.on()
RedLED.low()

while True:
    if uart.any() >= 64:
        data = uart.read(64)
        if CONFIG in data:
            ack()
            break
    if is_pressed(RemoteTrigger):
        break
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
    if is_pressed(StartButton):
        StartStopLED.low()
        GreenLED.low()
        timer(seconds=5)
    if is_pressed(GreenButton):
        StartStopLED.low()
        GreenLED.low()
        timer(seconds=3)

    time.sleep(0.05)
