import time
import network
import credentials
import ubinascii
import machine

wlan = network.WLAN(network.STA_IF)
wlan.active(True)

print("connecting to network..")
wlan.connect(credentials.ESSID, credentials.Password)
while not wlan.isconnected():
    time.sleep(0.5)
print("connected.")

relay = machine.Pin(0, machine.Pin.OUT)
relay.off()

MQTT_CONFIG = {
     "USER": "",
     "PASSWORD": "",
     "PORT": 1883,
     "TOPIC": b"relay",
     # unique identifier of the chip
     "CLIENT_ID": b"esp8266_" + ubinascii.hexlify(machine.unique_id())
}

newMessage = None

def onMQTTMessage(topic, msg):
    global newMessage
    print("Topic: %s, Message: %s" % (topic, msg))
    if msg == b"on":
        relay.on()
    elif msg == b"off":
        relay.off()
    newMessage = msg

def each_loop(client):
    global newMessage
    if newMessage in [b'on', b'off']:
        client.publish(MQTT_CONFIG['TOPIC'] + b'/state', newMessage)
        newMessage = None

from mqtt import listen
listen(onMQTTMessage, each_loop, MQTT_CONFIG)