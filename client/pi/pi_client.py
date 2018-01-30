#!/usr/bin/python

from sys import argv, stderr
from os.path import expanduser, isfile
from glob import glob

import re
from Hydranet.configuration import Config
from Hydranet.messenger import Messenger

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
    #print "Section:", section
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
                m = Messenger("jtwo.org")
                m.update(config.getint(section,'ID'), temperature)
