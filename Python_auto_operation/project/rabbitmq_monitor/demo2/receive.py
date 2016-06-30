#!/usr/bin/env python
# coding: utf-8

import pika
import time

connection = pika.BlockingConnection(pika.ConnectionParameters(
    host='192.168.10.28'
))
channel = connection.channel()

channel.queue_declare(queue='task_queue', durable=True)
print '[*] Waiting for message. To exit press CTRL+C'

def callback(ch, method, properties, body):
    print "[x] Received %r" %(body,)
    time.sleep(body.count('.'))
    print "[x] Done"
    ch.basic_ack(delivery_tag=method.delivery_tag)     #消息处理完毕后发送ack,rabbitmq才会把队列消息移出

channel.basic_qos(prefetch_count=1)  #在多个consumer之间进行roundrobin时,rabbitmqserver在没收到consumer的ack之前,则不会向其推送消息
channel.basic_consume(callback,
                      queue='task_queue')
channel.start_consuming()