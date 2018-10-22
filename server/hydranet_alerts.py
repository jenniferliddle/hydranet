#!/usr/bin/env python
'''
hydranet_alerts.py

Check to see if we need to send any alerts
'''

import sys
from os.path import expanduser
import json
import ConfigParser
import daemon
import logging
import logging.handlers
import time
import os
import smtplib
from email.mime.text import MIMEText
from Hydranet.db import DB, Data, Alert, Alerts_Sent

def openDatabase():
    ''' Open the database, ready for storing data '''
    # Read the configuration file
    config = ConfigParser.ConfigParser()
    config.read(expanduser('~/hydranetrc'))

    dbname = 'Database_rw'
    db = DB()
    db.connect({'host':config.get(dbname, 'host'),
            'user':config.get(dbname, 'user'),
            'password':config.get(dbname, 'password'),
            'database':config.get(dbname, 'database')})
    return db

def closeDatabase(db):
    ''' Close the database '''
    db.close()

def checkAlert(row, d):
    drows = []
    print "Checking alert: ", row
    if row['Period'] == 0:
        drows.append(d.loadLatest(row['Sensor_ID']))
    else:
        drows = d.loadPeriod(row['Sensor_ID'], row['Period'])
    print "Found", len(drows), "data points"
    for r in drows:
        print "\t", r

if __name__ == "__main__":
    db = openDatabase()
    d = Data(db)
    a = Alert(db)
    alerts = a.loadAll()
    for row in alerts:
        checkAlert(row,d)
    closeDatabase(db)
