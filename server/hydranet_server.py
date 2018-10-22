#!/usr/bin/env python
'''
hydranet_server.py

The Hydranet server reads and processes messages from the RabbitMQ 'hydranet' queue
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
from Hydranet.db import DB, Data

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

def update(msg):
    ''' Process an 'update' command
        The values are expected to be
        sensor      the Sensor_ID
        value       an integer or float value
        date        an asctime() string
    '''
    db = openDatabase()
    data = Data(db)
    msg.setdefault('date','')
    print "Inserting data: ", msg['sensor'],msg['sensor'], msg['value'], msg['date']
    data.insert(msg['sensor'],msg['sensor'], msg['value'], msg['date'])
    closeDatabase(db)

def on_message(channel, method_frame, header_frame, body):
    ''' callback function to handle command messages
        The message body is a json format string.

        Valid command messages are:
        
        update      update the database with a sensor reading
    '''
    channel.basic_ack(delivery_tag=method_frame.delivery_tag)

    msg = json.loads(body)
    if (msg['command'] == 'update'):
        update(msg);

def start_process():
    import pika

    # Open the RabbitMQ connection and set callback functions
    connection = pika.BlockingConnection()
    channel = connection.channel()
    channel.queue_declare(queue='hydranet')
    channel.basic_consume(on_message, 'hydranet')

    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        channel.stop_consuming()

if __name__ == "__main__":
    #
    # Set up logging
    #
    LOG_FILENAME = '/tmp/hydranet.log'
    hlog = logging.getLogger(__name__)
    hlog.setLevel(logging.DEBUG)
    handler = logging.handlers.RotatingFileHandler(LOG_FILENAME, maxBytes=10000, backupCount=3)
    formatter = logging.Formatter('[%(asctime)s] - %(message)s')
    handler.setFormatter(formatter)
    hlog.addHandler(handler)
    hlog.warn(time.asctime()+' Starting hydranet_server')
    hlog.info(os.environ)

    # Loop to process messages
    c = daemon.DaemonContext(
        stdout=open(LOG_FILENAME, 'a', 0),
        stderr=open(LOG_FILENAME, 'a', 0),
        umask=0o002,
    )
    with c:
        start_process()

