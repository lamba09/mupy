from umqtt.simple import MQTTClient

def listen(onMessage, each_loop, config):
    #Create an instance of MQTTClient
    client = MQTTClient(config['CLIENT_ID'], config['MQTT_BROKER'], user=config['USER'], password=config['PASSWORD'], port=config['PORT'])
    # Attach call back handler to be called on receiving messages
    client.set_callback(onMessage)
    client.connect()
    client.publish(config['TOPIC'], "ESP8266 is Connected")
    client.publish(config['TOPIC'], "off")
    client.subscribe(config['TOPIC'])
    print("ESP8266 is Connected to %s and subscribed to %s topic" % (config['MQTT_BROKER'], config['TOPIC']))

    try:
        while True:
            #msg = client.wait_msg()
            msg = client.check_msg()
            each_loop(client)
    finally:
        client.disconnect()
