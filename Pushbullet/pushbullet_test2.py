from pushbullet import Pushbullet
import RPi.GPIO as GPIO
from time import sleep
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.IN) 
pb = Pushbullet("o.KU91fAypbbfUBGWQkAkj6Ajec6uPrul9")
print(pb.devices)

while True:
    dev = pb.get_device('Motorola Moto g(9)')
    push = dev.push_note("Alert!!", "Someone is in your house")
    sleep(1)
    #dev.pushFile('Motorola Moto g(9)', "idc", "ida", open(home/pi/Desktop/hilda2.jpg, "rb"))
    with open("SnapshotTest.jpg", "rb") as pic:
        file_data=pb.upload_file(pic,"picture.jpg")
    push=pb.push_file(**file_data)
    sleep(1)