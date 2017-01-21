#!/usr/bin/python

import time
import Adafruit_BBIO.ADC as ADC
import Adafruit_BBIO.GPIO as GPIO
import Hydranet

#AIN0 13.8v batery  Pin 39
#AIN1 18v pannels   Pin 40
#AIN3 13.8v current sensor Pin 38
#AIN2 20A current sensor pin 37
#GPIO7 Geiger Counter pin 42
#GPIO60 Temperature pin 12

geigerMinuteCount = 0
secondCounter = 0

def increaseCount(response):
    global geigerMinuteCount
    geigerMinuteCount += 1
    #print "Counter updated: %d" % geigerMinuteCount

ADC.setup()
GPIO.setup("P9_42",GPIO.IN)
GPIO.add_event_detect("P9_42", GPIO.RISING, callback=increaseCount)

try:
    value = 0
    while True:
        if secondCounter > 60 :
            #average readings and send them to HydraNetServer
            print "Geiger Count: %d, Voltage %d" % ( geigerMinuteCount,value)
            hydranet.update("Geiger Counter",geigerMinuteCount)
            geigerMinuteCount = 0
            secondCounter = 0
        else :
            #read returns values 0-1.0
            value = ADC.read("P9_39")
            #print value * 20
            secondCounter += 1
            time.sleep(1)

except KeyboardInterrupt:
    GPIO.cleanup()

