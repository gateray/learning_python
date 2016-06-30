#!/usr/bin/env python
# coding: utf-8

import pika
import sys

connection = pika.BlockingConnection(pika.ConnectionParameters(
    host='192.168.10.28'
))

channel = connection.channel()

channel.queue_declare(queue='task_queue', durable=True)  #队列持久化

message = ' '.join(sys.argv[1:]) or "Hello World!"
channel.basic_publish(exchange='',
                      routing_key='task_queue',
                      body=message,
                      properties=pika.BasicProperties(
                          delivery_mode = 2   #使得消息持久化
                      ))
print "[x] Sent %r" %(message,)
connection.close()