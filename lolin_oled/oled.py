# oled display of LOLIN mini board
from machine import Pin, I2C
import ssd1306

WIDTH = 64
HEIGHT = 48
ADDRESS = 0x3c

i2c = I2C(scl=Pin(5), sda=Pin(4), freq=100000)
oled = ssd1306.SSD1306_I2C(WIDTH, HEIGHT, i2c, ADDRESS)

def hello_world():
    import time
    rects = [oled.rect, oled.fill_rect, oled.fill_rect]
    for _ in range(30):
        oled.fill(0)
        oled.text("Hello", 0, 0)
        oled.text("World", 25, 10)
        oled.hline(5, 25, 54, 0xffff)

        rects[0](24, 36, 5, 5, 0xffff)
        rects[1](30, 36, 5, 5, 0xffff)
        rects[2](36, 36, 5, 5, 0xffff)

        oled.show()

        rects = [rects[2], rects[0], rects[1]]

    time.sleep(0.33)