import machine, ssd1306

i2c = machine.I2C(scl=machine.Pin(4), sda=machine.Pin(5))

WIDTH = 128
HEIGHT = 64

oled = ssd1306.SSD1306_I2C(WIDTH, HEIGHT, i2c)

def hello_world():
    console('MicroPython on')
    console('an ESP32 with an')
    console('attached SSD1306')
    console('OLED display')

_console_buf = []
_mcll = WIDTH // 8  # max character line length (character width = 8px)
def console(text):
    global _console_buf
    if "\n" in text:
        lines = text.split("\n")
        for line in lines:
            console(line)
        return
    if len(text) > _mcll:
        lines = [text[i*_mcll:i*_mcll+_mcll] for i in range(int(len(text)/_mcll + 1))]
        for line in lines:
            console(line)
        return
    if len(_console_buf) == 6:
        _console_buf = _console_buf[1:] + [text]
    else:
        _console_buf.append(text)
    oled.fill(0)
    for i, t in enumerate(_console_buf):
        oled.text(t, 0, i*10)
    oled.show()

def clear_console():
    global _console_buf
    _console_buf = []
    oled.fill(0)
    oled.show()