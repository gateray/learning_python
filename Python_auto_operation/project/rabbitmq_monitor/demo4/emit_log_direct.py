#!/usr/bin/env python
# coding; utf-8

import pika
import sys

connection = pika.BlockingConnection(pika.ConnectionParameters(
    host = '192.168.10.28'
))

channel = connection.channel()
channel.exchange_declare(exchange='direct_logs',
                         type='direct')

severity = sys.argv[1] if len(sys.argv) > 1 else 'info'
message = ' '.join(sys.argv[1:]) or 'hello world!'
"""
Direct exchange的路由算法非常简单：通过binding key的完全匹配
exchange X和两个queue绑定在一起。Q1的binding key是orange。Q2的binding key是black和green。
    当P publish key是orange时，exchange会把它放到Q1。如果是black或者green那么就会到Q2。其余的Message都会被丢弃。
"""
channel.basic_publish(exchange='direct_logs',
                      routing_key=severity,
                      body=message)
print '[x] sent %r:%r' %(severity, message)
connection.close()
