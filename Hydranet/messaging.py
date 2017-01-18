#!/usr/bin/python

""" Module for updating Hydranet with sensor data.
"""

from urllib import urlencode
from urllib2 import urlopen, Request
from datetime import datetime
from sys import stderr
import ConfigParser

# PROPERTIES
ip = "192.168.2.166"
update_path = "/cgi/update"
date_format = "%d-%m-%Y %H:%M:%S"
debug = False

""" Update Hydranet. Parameters:

		sensor - sensor identifier, e.g. "Pi"
		value - temperature, humidity, weight, etc
		echo - if True, echo update data
"""
def update(sensor, value, echo=False):
	timestamp = datetime.now().strftime(date_format)
	data = { "sensor": sensor, "value": value, "date": timestamp, "key": 101 }

	if echo or debug:
		print "%s: %s at %s" % (sensor, value, timestamp)

	# build GET request and echo URL
	req = Request("http://%s%s?%s" % (ip, update_path, urlencode(data)))
	if debug:
		print "GET", req.get_full_url()

	# do the GET, ignore the (empty) response
	if not debug:
		urlopen(req).read()

