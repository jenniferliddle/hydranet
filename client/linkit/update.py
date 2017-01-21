#!/usr/bin/python

""" Module for updating Hydranet with sensor data.
"""

import sys
from urllib import urlencode
from urllib2 import urlopen, Request
from datetime import datetime

# PROPERTIES
IP = "192.168.2.166"
UPDATE_PATH = "/cgi/update"
DATE_FORMAT = "%d-%m-%Y %H:%M:%S"
DEBUG = False

""" Update Hydranet. Parameters:

        sensor - sensor identifier, e.g. "Pi"
        value - temperature, humidity, weight, etc
        echo - if True, echo update data
"""
def update(sensor, value, echo=False):
    timestamp = datetime.now().strftime(DATE_FORMAT)
    data = { "sensor": sensor, "value": value, "date": timestamp, "key": 104 }

    if echo or DEBUG:
        print "%s: %s at %s" % (sensor, value, timestamp)

    # build GET request and echo URL
    req = Request("http://%s%s?%s" % (IP, UPDATE_PATH, urlencode(data)))
    if DEBUG:
        print "GET", req.get_full_url()

    # do the GET, ignore the (empty) response
    if not DEBUG:
        urlopen(req).read()

if __name__ == "__main__":
    sensor = sys.argv[1]
    temp = sys.argv[2]
    update(sensor,temp)

