#!/usr/bin/python3

from apds9960.const import *
from apds9960 import APDS9960
import RPi.GPIO as GPIO
import smbus
import datetime
import time
from time import sleep

port = 1
bus = smbus.SMBus(port)

apds = APDS9960(bus)


def intH(channel):
    print()


GPIO.setmode(GPIO.BOARD)
GPIO.setup(7, GPIO.IN)
try:
    # Interrupt-Event hinzufuegen, steigende Flanke
    GPIO.add_event_detect(7, GPIO.FALLING, callback=intH)
    apds.enableLightSensor()
    sleep(1)
    outstring = "{ \"place\" : \"home\" ,"
    outstring += "  \"time\" : \"{}\" ,".format(
        datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"))
    outstring += "  \"AmbientLight\" : {} ,".format(apds.readAmbientLight())
    outstring += "  \"red\" :{} ,".format(apds.readRedLight())
    outstring += "  \"green\" :{} ,".format(apds.readGreenLight())
    outstring += "  \"blue\" :{} ".format(apds.readBlueLight()) + "}"
    print(outstring)

finally:
    GPIO.cleanup()
