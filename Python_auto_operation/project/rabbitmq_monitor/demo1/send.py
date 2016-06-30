#!/usr/bin/env python
# coding: utf-8

import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(
    host = '192.168.10.28'
))
channel = connection.channel()
channel.queue_declare(queue='hello')
channel.basic_publish(exchange='',
                      routing_key='hello',
                      body='Hello World!')
print "[x] Sent 'Hello World!"
connection.close()