'''
Class to handle sending messages to (and possibly from)
the Hydranet server using RabbitMQ

Author: Jennifer Liddle <jennifer@jsquared.co.uk>

'''
import pika
import json

class Messenger(object):
    ''' Class to wrap pika for sending messages'''
    def __init__(self, host='localhost', queue='hydranet'):
        '''Initialise pika, providing defaults for host and queue'''
        self.host = host
        self.queue = queue
        self.con = pika.BlockingConnection(pika.ConnectionParameters(self.host))
        self.channel = self.con.channel()

    def __del__(self):
        ''' Close the rabbitmq connection '''
        self.con.close()

    def send(self, body):
        ''' Send raw text to the Hydranet server '''
        self.channel.basic_publish('',self.queue, body)

    def update(self, sensor, value):
        ''' send sensor update to hydranet '''
        body = json.dumps({'command':'update', 'sensor': sensor, 'value': value})
        self.send(body)

