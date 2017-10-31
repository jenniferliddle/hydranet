'''
Class to handle sending messages to (and possibly from)
the Hydranet server using RabbitMQ

Author: Jennifer Liddle <jennifer@jsquared.co.uk>

'''
import pika
import json
import time
import datetime

class Messenger(object):
    ''' Class to wrap pika for sending messages'''
    def __init__(self, host='192.168.2.230', queue='hydranet'):
        '''Initialise pika, providing defaults for host and queue
           TODO: host *must* be read from config file, not hard coded
        '''
        credentials = pika.PlainCredentials('hydranet', 'hydranet')
        self.host = host
        self.queue = queue
        self.con = pika.BlockingConnection(pika.ConnectionParameters(self.host,5672,'/',credentials))
        self.channel = self.con.channel()

    def __del__(self):
        ''' Close the rabbitmq connection '''
        self.con.close()

    def send(self, body):
        ''' Send raw text to the Hydranet server '''
        self.channel.basic_publish('',self.queue, body)

    def update(self, sensor, value):
        ''' send sensor update to hydranet '''
        ts = time.time()
        timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        body = json.dumps({'command':'update', 'sensor': sensor, 'value': value, 'date': timestamp})
        self.send(body)

