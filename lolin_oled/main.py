from oled import oled, hello_world, wait
import credentials
import network
import time
import ubinascii
import machine

led = machine.Pin(2, machine.Pin.OUT)
led.on()

wlan = network.WLAN(network.STA_IF)
wlan.active(True)

UDP_PORT = 37020

HTTP_MODE="http"
UDP_MODE="udp"
MQTT_MODE="mqtt"

mode=MQTT_MODE

MQTT_CONFIG = {
     "USER": "",
     "PASSWORD": "",
     "PORT": 1883,
     "TOPIC": b"test",
     # unique identifier of the chip
     "CLIENT_ID": b"esp8266_" + ubinascii.hexlify(machine.unique_id())
}

hello_world()

print("connecting to network..")
wlan.connect(credentials.ESSID, credentials.Password)
while not wlan.isconnected():
    wait(0.33)

ip, netmask, gateway, dns = wlan.ifconfig()
print("connected to", credentials.ESSID, "with ip", ip)

def display_ip():
    oled.text("IP:", 0, 0)
    oled.text("{:>3}.{:>3}.".format(*ip.split(".")[:2]), 0, 10)
    oled.text("{:>3}.{:>3}".format(*ip.split(".")[2:]), 0, 20)

def show_value(value):
    oled.fill(0)
    display_ip()
    oled.text(value, 0, 40)
    oled.show()

def data_handler(data):
    oled.fill(0)
    oled.text("listen", 0, 0)
    oled.text("UDP Port", 0, 10)
    oled.text(str(UDP_PORT), 0, 20)
    oled.text(data.decode(), 0, 40)
    oled.show()

newMessage = None
lastDisplay = ""

def onMQTTMessage(topic, msg):
    global newMessage
    global lastDisplay
    newMessage = msg
    print("Topic: %s, Message: %s" % (topic, msg))
    oled.fill(0)
    oled.text('Pi4IoT', 0, 0)
    if msg == b"on":
        led.off()
        oled.text('LED: ON', 0, 20)
        oled.text(lastDisplay, 0, 30)
    elif msg == b"off":
        led.on()
        oled.text('LED: OFF', 0, 20)
        oled.text(lastDisplay, 0, 30)
    else:
        state = "LED: OFF" if led.value() else "LED: ON"
        lastDisplay = msg.decode()
        oled.text(state, 0, 20)
        oled.text(lastDisplay, 0, 30)
    oled.show()

def each_loop(client):
    global newMessage
    if newMessage in [b'on', b'off']:
        client.publish(MQTT_CONFIG['TOPIC'] + b'/state', newMessage)
        newMessage = None
    elif newMessage is not None:
        client.publish(MQTT_CONFIG['TOPIC'] + b'/display', newMessage)
        newMessage = None

if mode == HTTP_MODE:
    from set_led_http import serve
    show_value("")
    serve(show_value)

elif mode == UDP_MODE:
    oled.fill(0)
    oled.text("listen", 0, 0)
    oled.text("UDP Port", 0, 10)
    oled.text(str(UDP_PORT), 0, 20)
    oled.show()

    from udp_client import listen
    listen(data_handler, port=UDP_PORT)

elif mode == MQTT_MODE:
    from mqtt import listen
    listen(onMQTTMessage, each_loop, MQTT_CONFIG)