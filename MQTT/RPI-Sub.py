import paho.mqtt.client as mqtt
MQTT_ADDRESS = '192.168.25.62'
MQTT_USER = 'RPi'
MQTT_PASSWORD = 'RPi'
MQTT_TOPIC_LIGHT = 'rfid'


def on_connect(client,userdata,flags,rc):
    print('connected with result code ' + str(rc))
    client.subscribe(MQTT_TOPIC_LIGHT)
    
    
def on_message(client, userdata, msg):
    print(msg.topic + ':' + str(msg.payload.decode('utf-8')))
    
def main():
    mqtt_client = mqtt.Client()
    mqtt_client.username_pw_set(MQTT_USER, MQTT_PASSWORD)
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = on_message
    
    mqtt_client.connect('192.168.25.62', 1883)
    mqtt_client.loop_forever()
    
if __name__== '__main__':
    print('MQTT to InfluxDB bridge')
    main()