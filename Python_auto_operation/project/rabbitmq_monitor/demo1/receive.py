#!/usr/bin/env python
# coding: utf-8

import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(
    host='192.168.10.28'
))

channel = connection.channel()
channel.queue_declare(queue='hello')

print '[x] waiting for message. to exit press Ctrl+c'

def callback(ch, method, properties, body):
    print "[x] received %r" %(body,)

channel.basic_consume(callback,
                      queue='hello',
                      no_ack=True)
channel.start_consuming()
