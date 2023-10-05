import paho.mqtt.client as mqtt

MQTT_ADDRESS = '192.168.25.62'
MQTT_USER = 'RPi'
MQTT_PASSWORD = 'RPi'
MQTT_TOPIC_RFID = 'rfid'

# Variable to store RFID data
rfid_data = ""

def on_connect(client, userdata, flags, rc):
    print('Connected with result code ' + str(rc))
    client.subscribe(MQTT_TOPIC_RFID)

def on_message(client, userdata, msg):
    global rfid_data  # Declare the variable as global to modify it within this function
    rfid_data = msg.payload.decode('utf-8')
    print(msg.topic + ': ' + rfid_data)

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
