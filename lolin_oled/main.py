from oled import oled, hello_world, wait
from wlan import wlan, credentials

hello_world()

wlan.connect()
while not wlan.isconnected():
    wait(0.33)

ip, netmask, gateway, dns = wlan.ifconfig()
print("connected to", credentials.ESSID, "with ip", ip)

def display_ip():
    oled.text("IP:", 0, 0)
    oled.text("{:>3}.{:>3}.".format(*ip.split(".")[:2]), 0, 10)
    oled.text("{:>3}.{:>3}".format(*ip.split(".")[2:]), 0, 20)

#def show_value(value):
#    oled.fill(0)
#    display_ip()
#    oled.text(value, 0, 40)
#    oled.show()
#
#from set_led_http import serve
#serve(show_value)

UDP_PORT = 37020

oled.fill(0)
oled.text("listen", 0, 0)
oled.text("UDP Port", 0, 10)
oled.text(str(UDP_PORT), 0, 20)
oled.show()

def data_handler(data):
    oled.fill(0)
    oled.text("listen", 0, 0)
    oled.text("UDP Port", 0, 10)
    oled.text(str(UDP_PORT), 0, 20)
    oled.text(data.decode(), 0, 40)
    oled.show()

from udp_client import listen
listen(data_handler, port=UDP_PORT)