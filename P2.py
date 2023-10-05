import socket
import datetime
from datetime import date
import board  # Import the board module
import RPi.GPIO as GPIO
from time import sleep
import Adafruit_DHT
import adafruit_bh1750

# Configure UDP server
udp_server_ip = '0.0.0.0'  # Listen on all available network interfaces
udp_server_port = 12345  # Choose a suitable port

# Create a UDP socket
udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp_socket.bind((udp_server_ip, udp_server_port))

# Variable to store RFID data
rfid_data = None  # Initialize to None initially
rfid_lock = False  # Lock to prevent data modification
temperature = None
humidity = None
lux_value = None


GPIO.setwarnings(False)


buzzer = 36
GPIO.setup(buzzer, GPIO.OUT)
# DHT11 sensor selected
sensor = Adafruit_DHT.DHT11
# DHT sensor pin connected to GPIO 17
dht = 31
led = 37
GPIO.setup(led, GPIO.OUT)


def buzz_and_flash(buzzer_pin, led_pin, duration):
    for _ in range(duration):
        GPIO.output(buzzer_pin, GPIO.HIGH)
        GPIO.output(led_pin, GPIO.HIGH)
        sleep(0.1)
        GPIO.output(buzzer_pin, GPIO.LOW)
        GPIO.output(led_pin, GPIO.LOW)
        sleep(0.1)

def read_sensors(var):
    global temperature, humidity, lux_value
    try:
        today_date = date.today()
        now_time = datetime.datetime.now().time()
        date_str = today_date.strftime("%Y-%m-%d")
        time_str = now_time.strftime("%H:%M:%S")
        
        # BH1750 Lux sensor
        i2c = board.I2C()
        lux_sensor = adafruit_bh1750.BH1750(i2c)
        lux_value = lux_sensor.lux
        print('Lux: {:.2f}'.format(lux_value))

        # DHT11 sensor
        sensor = Adafruit_DHT.DHT11
        gpio = 31
        humidity, temperature = Adafruit_DHT.read_retry(sensor, gpio)

        if humidity is not None and temperature is not None:
            print('Temperature: {:.1f}°C, Humidity: {:.1f}%'.format(temperature, humidity))
        else:
            print('Failed to get DHT11 reading. Try again!')
        #send_notification_with_variables(access_key, "Motorola Moto g(9)", "Parameters", "These are the current sensor readings of the industry", temperature, humidity, lux_value)
        udptest(var, "Parameters are:", date_str, time_str, temperature, humidity, lux_value)
    except Exception as e:
        print('An error occurred:', str(e))


def udptest(address, message, variable1, variable2, variable3, variable4, variable5,):
    # Prepare a response
    response_data = f"{message} Date: {variable1} Time: {variable2} Temperature: {variable3} Humidity: {variable4} Ambient Light: {variable5}"

    # Send the response back to the ESP32
    udp_socket.sendto(response_data.encode(), address)

def main():
    # Receive UDP packet from ESP32
    data, address = udp_socket.recvfrom(1024)  # Adjust buffer size as needed
    print(f"Received from {address}: {data.decode()}")
    if data == b'f2 b5 8a 33':
        read_sensors(address)
    else:
       buzz_and_flash(buzzer, led, 5) 

if __name__ == '__main__':
    print('MQTT to InfluxDB bridge')
    main()
    sleep(2)
