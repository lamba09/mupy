import time
import network
import credentials

wlan = network.WLAN(network.STA_IF)
wlan.active(True)

print("connecting to network..")
wlan.connect(credentials.ESSID, credentials.Password)
while not wlan.isconnected():
    time.sleep(0.5)
print("connected.")

import blink