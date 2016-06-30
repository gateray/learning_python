#!/usr/bin/env python
# coding: utf-8

import pika
import sys

connection = pika.BlockingConnection(
    pika.ConnectionParameters(
        host = '192.168.10.28'
    )
)

channel = connection.channel()
channel.exchage_declare(exchange='direct_logs',
                        type='direct')

result = channel.queue_declare(exclusive=True)
queue_name = result.method.queue

severities = sys.argv[1:]
if not severities:
    print >> sys.stderr, "usage: %s [info] [warn] [error]" %(sys.argv[0],)
    sys.exit(1)

for severity in severities:
    channel.queue_bind(exchange='direct_logs',
                       queue=queue_name,
                       routing_key=severity)

print '[x] waiting for logs. to exit press ctrl+c'

def callback(ch,method,properties, body):
    print '[x] %r:%r' %(method.routing_key, body,)

channel.basic_consume(callback,
                      queue=queue_name,
                      no_ack=True)

channel.start_consuming()

