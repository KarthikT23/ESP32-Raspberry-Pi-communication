import paho.mqtt.client as mqtt

# MQTT Configuration for Temperature and Humidity
MQTT_ADDRESS = '192.168.72.62'
MQTT_USER = 'KarthikT'
MQTT_PASSWORD = 'deathnote'
MQTT_TOPIC_TEMP = 'Temperature'
MQTT_TOPIC_HUMD = 'Humidity'

# MQTT Configuration for RFID
MQTT_TOPIC_RFID = 'rfid'

def on_connect(client, userdata, flags, rc):
    print('Connected with result code ' + str(rc))
    client.subscribe(MQTT_TOPIC_TEMP)
    client.subscribe(MQTT_TOPIC_HUMD)
    client.subscribe(MQTT_TOPIC_RFID)

def on_message(client, userdata, msg):
    print(msg.topic + ' ' + str(msg.payload))

def main():
    mqtt_client = mqtt.Client()
    mqtt_client.username_pw_set(MQTT_USER, MQTT_PASSWORD)
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = on_message

    mqtt_client.connect(MQTT_ADDRESS, 1883)
    mqtt_client.loop_forever()

if __name__ == '__main__':
    print('MQTT to InfluxDB bridge')
    main()
