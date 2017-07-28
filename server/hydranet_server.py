import sys
from os.path import expanduser
import pika
import json
import ConfigParser

sys.path.insert(0, '/usr/local/lib/python2.7')
from Hydranet.db import DB, Data

def openDatabase():
    global config
    dbname = 'Database_rw'
    db = DB()
    db.connect({'host':config.get(dbname, 'host'),
            'user':config.get(dbname, 'user'),
            'password':config.get(dbname, 'password'),
            'database':config.get(dbname, 'database')})
    return db

def update(msg):
    db = openDatabase()
    data = Data(db)
    data.insert(msg['sensor'],msg['sensor'], msg['value'])

def on_message(channel, method_frame, header_frame, body):
    print method_frame.delivery_tag, body
    channel.basic_ack(delivery_tag=method_frame.delivery_tag)

    msg = json.loads(body)
    if (msg['command'] == 'update'):
        update(msg);


# Read the configuration file
config = ConfigParser.ConfigParser()
config.read(expanduser('~/hydranetrc'))

# Open the RabbitMQ connection
connection = pika.BlockingConnection()
channel = connection.channel()
channel.queue_declare(queue='hydranet')
channel.basic_consume(on_message, 'hydranet')
try:
    channel.start_consuming()
except KeyboardInterrupt:
    channel.stop_consuming()
connection.close()

