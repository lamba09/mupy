import time
from machine import Pin, I2C
import ssd1306

WIDTH = 64
HEIGHT = 48
ADDRESS = 0x3c

i2c = I2C(scl=Pin(5), sda=Pin(4), freq=100000)
oled = ssd1306.SSD1306_I2C(WIDTH, HEIGHT, i2c, ADDRESS)


def hello_world():
    for _ in range(9):
        wait(0.33)

_wait_step = 0
_rect_steps = [
    [oled.rect, oled.fill_rect, oled.fill_rect],
    [oled.fill_rect, oled.rect, oled.fill_rect],
    [oled.fill_rect, oled.fill_rect, oled.rect],
]
def wait(t):
    global _wait_step
    global _rect_steps
    oled.fill(0)
    oled.text("Hello", 0, 0)
    oled.text("World", 25, 10)
    oled.hline(5, 25, 54, 0xffff)

    _rect_steps[_wait_step][0](24, 36, 5, 5, 0xffff)
    _rect_steps[_wait_step][1](30, 36, 5, 5, 0xffff)
    _rect_steps[_wait_step][2](36, 36, 5, 5, 0xffff)

    oled.show()

    _wait_step += 1
    _wait_step %= 3

    time.sleep(t)