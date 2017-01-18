#!/usr/bin/python

from sys import argv
from subprocess import Popen, PIPE
from re import compile as re_compile
import hydranet

# PROPERTIES
sensor_prefix = "DMZ_"

if len(argv) < 2 or argv[1] != "-u":
	print "DEBUG: to update Hydranet, run %s -u" % argv[0]
	hydranet.debug = True

re = re_compile(r"Sensor\s+(\d+)\s+C:\s+([\d.]+)")

# collect sensor readings using digitemp - 10 for each sensor
sensors = {}
proc = Popen(['digitemp', '-q', '-a', '-n 10'], stdout=PIPE)
for line in iter(proc.stdout.readline, ''):
	values = re.findall(line)
	if len(values) == 0:
		continue
	sensor_n, temp = values[0]
	temp = float(temp)
	try:
		sensors[sensor_n].append(temp)
	except KeyError:
		sensors[sensor_n] = [temp]

# take the median of each set of readings and update hydranet
for sensor_n, temps in sensors.iteritems():
	sensor_id = "%s%s" % (sensor_prefix, sensor_n)
	temperature = hydranet.median(temps)
	hydranet.update(sensor_id, temperature, echo=True)

