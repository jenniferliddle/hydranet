#!/usr/bin/python

from sys import argv, stderr
from os.path import expanduser, isfile
from glob import glob

import re
from hydranet.configuration import Config
from hydranet.messaging import update

# CONSTANTS
COUNT_KEY = "count"

# parse command line
if len(argv) < 2 or argv[1] != "-u":
	print "DEBUG: to update Hydranet, run %s -u" % argv[0]

# parse config file
config = Config()

# get a temperature reading from the sensor
def read_temperature(device_path):
	while True:
		with open(device_path, "rb") as f:
			lines = f.readlines()
		if "YES" in lines[0]:
			return float(lines[1].split("=")[1]) / 1000

# iterate devices
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
            update(config.getint(section,'ID'), temperature, echo=True)
