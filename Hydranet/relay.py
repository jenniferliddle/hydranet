#!/usr/bin/env python

"""

Hydranet.relay

Module to drive relays connected to serial port

Author: Jennifer Liddle

"""

class Relay(object):

    DEVICE = '/dev/lights'
    DATAFILE = '/var/www/data/lights.dat'

    relays = {}

    def __init__(self):
        self.readStateFile()

    def readStateFile(self):
        fh = open(self.DATAFILE,"r")
        for line in fh.readlines():
            (key,val) = line.strip().split(',')
            self.relays[key] = val
        fh.close()


if __name__ == "__main__":
    relay = Relay()
    print "Relays: ", relay.relays


