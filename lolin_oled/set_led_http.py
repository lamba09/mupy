# original code from:
# https://github.com/Pi4IoT/Single_Board_Computer/blob/master/ESP8266/set_led_http.py
import socket
import machine


#HTML to send to browsers
html = """<!DOCTYPE html>
<html>
<head> <title>ESP8266 LED ON/OFF</title> </head>
<h2>LED's on and off with Micropython</h2></center>
<h3>(ESP8266)</h3></center>
<form>
LED:
<button name="LED" value="LED_ON" type="submit">LED ON</button>
<button name="LED" value="LED_OFF" type="submit">LED OFF</button><br><br>
State: %s<br><br>

value: <input type="text" name="value"><input type="submit">
</form>
</html>
"""

def serve(value_handler):
    #Setup PIN
    LED_BLUE = machine.Pin(2, machine.Pin.OUT)
    LED_BLUE.off()
    state = "OFF"

    value = ""

    #Setup Socket WebServer
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('', 80))
    s.listen(5)
    while True:
        conn, addr = s.accept()
        print("Got a connection from %s" % str(addr))
        request = conn.recv(1024)
        print("Content = %s" % str(request))
        request = str(request)
        LED_ON = request.find('/?LED=LED_ON')
        LED_OFF = request.find('/?LED=LED_OFF')
        value_offset = request.find('/?value=')
        if value_offset == 6:
            request = request[6+8:]
            value = request[:request.find('HTTP')].strip()

        if LED_ON == 6:
            print('TURN LED ON')
            LED_BLUE.off()
            state = "ON"
        if LED_OFF == 6:
            print('TURN LED OFF')
            LED_BLUE.on()
            state = "OFF"

        value_handler(value)

        response = html % state
        conn.send(response)
        conn.close()