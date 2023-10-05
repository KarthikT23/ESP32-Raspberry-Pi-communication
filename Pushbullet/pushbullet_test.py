from pushbullet import Pushbullet
import RPi.GPIO as GPIO
from time import sleep
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.IN) 
pb = Pushbullet("your access token")
print(pb.devices)

while True:
    i = GPIO.input(11)
    if i == 0:
        print "no motion"
        sleep(1)
    elif i == 1:
        print "motion"
        
        dev = pb.get_device('Oppo F1s')
        push = dev.push_note("Alert!!", "Someone is in your house")
        sleep(1)