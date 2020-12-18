from ws2812 import WS2812
import time

# SETTINGS:
spi_bus    = 1   # LED chain DATA an SPI(1) MOSI pin (X8)
n          = 12  # anzahl LEDs in der kette:
brightness = 100 # helligkeit in der range 0 bis 255

# colors:
red = (brightness, 0, 0)
green = (0, brightness, 0)
blue = (0, 0, brightness)
yellow = (brightness, brightness, 0)
cyan = (0, brightness, brightness)
magenta = (brightness, 0, brightness)
white = (brightness, brightness, brightness)
black = (0, 0, 0)

colors = [red, green, blue, yellow, cyan, magenta, white, black]

# kurzschreibweise für n mal black in der liste:
# [black, black, ... , black]
# [(0,0,0), (0,0,0), ... , (0,0,0)]
data = [black]*n

ring = WS2812(spi_bus=spi_bus, led_count=n)


def set_all_color(color):
    all_same_color = [color]*n
    ring.show(all_same_color)


def set_one_pixel(index, color):
    """
    Diese funktion soll den pixel an position <index>
    auf eine bestimmte Farbe <color> setzen.
    Der index muss eine Zahl zwischen 0 und (n-1) sein.
    Die color ist eine der oben definierten Farben oder
    eine beliebige kombination:
                    (r, g, b)
    mit r, g, und b werte von 0 bis 255
    """
    data[index] = color
    ring.show(data) # neue data wird angezeigt


def cycle_color(color, t):
    """
    Diese Funktion soll durch jeden pixel gehen und die
    Farbe <color> setzen, wobei nach jedem setzen eine
    Zeit <t> in Sekunden gewartet wird.
    """
    for index in range(n):
        set_one_pixel(index, color)
        time.sleep(t)


def cycle_all_colors(t):
    for color in colors:
        cycle_color(color, t)
