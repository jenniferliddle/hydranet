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
        f = open(self.DATAFILE,"r")
        for line in f.readlines():
            (k,v) = line.strip().split(',')
            self.relays[k] = v
        f.close()


if __name__ == "__main__":
    relay = Relay()
    print "Relays: ", relay.relays


