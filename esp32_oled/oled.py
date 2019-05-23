import machine, ssd1306

i2c = machine.I2C(scl=machine.Pin(4), sda=machine.Pin(5))

WIDTH = 128
HEIGHT = 64

oled = ssd1306.SSD1306_I2C(WIDTH, HEIGHT, i2c)

def hello_world():
    oled.fill(0)
    oled.text('MicroPython on', 0, 0)
    oled.text('an ESP32 with an', 0, 10)
    oled.text('attached SSD1306', 0, 20)
    oled.text('OLED display', 0, 30)
    oled.show()

def console(text):
    import time
    oled.scroll(0, 10)
    oled.show()
    time.sleep(0.1)
    oled.text(text, 0, 54)
    oled.show()