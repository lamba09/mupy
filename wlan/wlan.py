import network
import credentials
import time

wlan = network.WLAN(network.STA_IF)
wlan.active(True)

def connect():
    print("connecting to network..")
    wlan.connect(credentials.ESSID, credentials.Password)

#while not wlan.isconnected():
#    time.sleep(0.1)
#ip, netmask, gateway, dns = wlan.ifconfig()
#print("connected to", credentials.ESSID, "with ip", ip)