import time
import network
import credentials
import ubinascii
from neopixel import NeoPixel
from machine import ADC, Pin
from mqtt import listen


np = NeoPixel(Pin(0), 38, bpp=4)
tv = ADC(0)  # TV voltage probe

default_color = (240, 65, 0, 15) # (255, 80, 25) / #ff5019
color = default_color

def show_color(color):
    c = color if tv.read() > 200 else (0,0,0,0)
    np.fill(c)
    np.write()

wlan = network.WLAN(network.STA_IF)
wlan.active(True)

print("connecting to network..")
wlan.connect(credentials.ESSID, credentials.Password)
while not wlan.isconnected():
    show_color(color)
    time.sleep(0.5)
print("connected.")

MQTT_CONFIG = {
     "MQTT_BROKER": "192.168.0.100",
     "USER": "",
     "PASSWORD": "",
     "PORT": 1883,
     "TOPIC": b"tv_lights",
     # unique identifier of the chip
     "CLIENT_ID": b"esp8266_" + ubinascii.hexlify(machine.unique_id())
}

def msg2color(msg):
    r = int(msg[1:3].decode(), 16)
    g = int(msg[3:5].decode(), 16)
    b = int(msg[5:7].decode(), 16)
    m = min(r, g, b)
    return (r-m, g-m, b-m, m)


def onMQTTMessage(topic, msg):
    global color
    print("Topic: %s, Message: %s" % (topic, msg))
    if msg.startswith(b"#") and len(msg) == 7:
        color = msg2color(msg)

def each_loop(client):
    show_color(color)
    time.sleep(0.5)

try:
    listen(onMQTTMessage, each_loop, MQTT_CONFIG)
except Exception as e:
    while True:
        show_color(default_color)
