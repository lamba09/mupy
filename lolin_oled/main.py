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

def show_value(value):
    oled.fill(0)
    display_ip()
    oled.text(value, 0, 40)
    oled.show()

show_value("")

from set_led_http import serve
serve(show_value)