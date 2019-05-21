from oled import oled

import wlan

def display_ip():
    ip = wlan.ip
    oled.text("IP:", 0, 0)
    oled.text("{:>3}.{:>3}.".format(*ip.split(".")[:2]), 0, 10)
    oled.text("{:>3}.{:>3}".format(*ip.split(".")[2:]), 0, 20)

oled.fill(0)
display_ip()
oled.show()
