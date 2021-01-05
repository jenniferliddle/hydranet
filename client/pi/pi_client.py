#!/usr/bin/python

from sys import argv, stderr
from os.path import expanduser, isfile
from glob import glob
import time
import re
from Hydranet.configuration import Config
from Hydranet.messenger import Messenger

try:
    import pyfirmata
except:
    print "pyfrmata not supported"

try:
    from bme280 import BME280
except:
    print "BME280 not supported"

try:
    from smbus2 import SMBus
except ImportError:
    from smbus import SMBus

# CONSTANTS
COUNT_KEY = "count"

local = False
# parse command line
if (len(argv)>1 and argv[1]=='-l'):
    local = True

# parse config file
config = Config()

'''
    Get a temperature reading from a one-wire sensor
    The reading is in the format:
        2c 01 4b 46 7f ff 04 10 14 : crc=14 YES
        2c 01 4b 46 7f ff 04 10 14 t=18750
'''
def read_temperature(device_path):
	while True:
		with open(device_path, "rb") as f:
			lines = f.readlines()
		if "YES" in lines[0]:
			return float(lines[1].split("=")[1]) / 1000

'''
    Look for devices in the configuration file, and process
    them one at a time...
'''
sections = config.sections()
for section in sections:
    print "Section:", section
    if (re.match('Sensor_', section)):
        sensor_type = config.getint(section, 'Type')

        if (sensor_type == 500):
            "This is a switch"
            pass

        if (sensor_type == 304):
            "This is a one-wire temperature sensor"
            temperature = read_temperature(config.get(section, 'device_path'))
            if local:
                print config.getint(section,'ID'), temperature
            else:
                m = Messenger("hydranet.co.uk")
                m.update(config.getint(section,'ID'), temperature)

        if (sensor_type == 504):
            "Arduino Firmata Voltage reader"
            device = config.get(section, 'device_path')
            board = pyfirmata.Arduino(device)
            pin = board.get_pin('a:0:i')
            pin.enable_reporting()
            it = pyfirmata.util.Iterator(board)
            it.start()
            time.sleep(1)
            v = pin.read()
            if v is not None:
                if local:
                    print v * 52.0, "V"
                else:
                    m = Messenger("hydranet.co.uk")
                    m.update(config.getint(section,'ID'), 52.0 * v)
            board.exit()

        if (sensor_type == 610):
            "BME280 humidity"
            bus = SMBus(1)
            bme280 = BME280(i2c_dev=bus)
            humidity_prev = -1
            humidity = bme280.get_humidity()
            while (int(humidity*10) != int(humidity_prev*10)):
                time.sleep(1)
                humidity_prev = humidity
                humidity = bme280.get_humidity()

            m = Messenger("hydranet.co.uk")
            m.update(config.getint(section,'ID'), humidity)

        if (sensor_type == 505):
            print "This is sensor 505"
