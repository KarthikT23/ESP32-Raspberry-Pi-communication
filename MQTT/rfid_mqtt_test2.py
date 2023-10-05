import paho.mqtt.client as mqtt
import socket
import RPi.GPIO as GPIO
from time import sleep
import Adafruit_DHT
import adafruit_bh1750
from pushbullet import Pushbullet
# Configure UDP server
udp_server_ip = '0.0.0.0'  # Listen on all available network interfaces
udp_server_port = 12345  # Choose a suitable port

# Create a UDP socket
udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp_socket.bind((udp_server_ip, udp_server_port))



MQTT_ADDRESS = '192.168.25.62'
MQTT_USER = 'RPi'
MQTT_PASSWORD = 'RPi'
MQTT_TOPIC_RFID = 'rfid'
MQTT_TOPIC_RESPONSE = 'rfid_response'  # Define a topic for the response

# Variable to store RFID data
rfid_data = None  # Initialize to None initially
rfid_lock = False  # Lock to prevent data modification

def on_connect(client, userdata, flags, rc):
    print('Connected with result code ' + str(rc))
    client.subscribe(MQTT_TOPIC_RFID)

def on_message(client, userdata, msg):
    global rfid_data, rfid_lock
    if not rfid_lock:  # Check if data is not locked
        rfid_lock = True  # Lock data
        rfid_data = msg.payload.decode('utf-8')
        print(msg.topic + ': ' + rfid_data)
        rfid_lock = False  # Unlock data
            # Call the function
        some_other_function()# Call a function to send a response to the ESP32
        
        udptest()

   
def main():
    mqtt_client = mqtt.Client()
    mqtt_client.username_pw_set(MQTT_USER, MQTT_PASSWORD)
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = on_message

    mqtt_client.connect(MQTT_ADDRESS, 1883)
    mqtt_client.loop_forever()

def some_other_function():
    global rfid_data  # Declare rfid_data as global if used in another function
    if rfid_data is not None:
        print("RFID Data:", rfid_data)
    else:
        print("RFID Data is not available yet.")

def udptest():
    
    # Receive UDP packet from ESP32
    data, address = udp_socket.recvfrom(1024)  # Adjust buffer size as needed
    print(f"Received from {address}: {data.decode()}")

    # Prepare a response
    response_data = "Response from Raspberry Pi"

    # Send the response back to the ESP32
    udp_socket.sendto(response_data.encode(), address)
    
if __name__ == '__main__':
    print('MQTT to InfluxDB bridge')
    main()

