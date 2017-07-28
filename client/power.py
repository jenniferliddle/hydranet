'''
power.py

Reads the power meter via the serial port
and sends updates to hydranet via RabbitMQ

<ch1> is the mains power
<ch2> is the solar power

This program reads the data for three minutes and calculates
an average. Then sends it, and exits.

It is designed to be run from a cron job.

Note that it has to run as root in order to acces
the serial port.
'''
import sys
sys.path.insert(0, '/usr/local/lib/python2.7')

import re
import serial
import time
from Hydranet.messenger import Messenger

MAINS_SENSOR = 405
SOLAR_SENSOR = 600
DEVICE = '/dev/ttyUSB.electricity'
BAUDRATE = 57600

mains_power = 0
mains_n = 0
solar_power = 0
solar_n = 0

def read_power():
    global mains_power
    global mains_n
    global solar_power
    global solar_n

    with serial.Serial(DEVICE, BAUDRATE, timeout=10) as ser:
        s=ser.read(255)
    if s:
        m=re.search('<ch1><watts>(\d+)</watts></ch1>',s)
        if m:
            v = int(m.groups()[0])
            if v: 
                mains_power += v
                mains_n += 1

        m=re.search('<ch2><watts>(\d+)</watts></ch2>',s)
        if m:
            v = int(m.groups()[0])
            if v:
                solar_power += v
                solar_n += 1

end_time = time.time() + 3*60
while time.time() < end_time:
    read_power()

m = Messenger()
if mains_n:
    m.update(MAINS_SENSOR, mains_power/mains_n)
if solar_n:
    m.update(SOLAR_SENSOR, solar_power/solar_n)

