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

sys.path.insert(0, '/usr/local/lib/python2.7')
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
    '''
    db = openDatabase()
    data = Data(db)
    data.insert(msg['sensor'],msg['sensor'], msg['value'])
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
    # Loop to process messages
    c = daemon.DaemonContext()
    with c:
        start_process()

