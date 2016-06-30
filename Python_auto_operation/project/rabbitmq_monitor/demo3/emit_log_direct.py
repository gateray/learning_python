#!/usr/bin/env python
# coding: utf-8

import pika
import sys

#发布/订阅模式+消息路由
connection = pika.BlockingConnection(pika.ConnectionParameters(
    host='192.168.10.28'
))

channel = connection.channel()
#定义一个exchange
"""
从Producer接收Message，然后投递到queue中。Exchange需要知道如何处理Message，是把它放到那个queue中，还是放到多个queue中？
这个rule是通过Exchange 的类型定义的。
我们知道有三种类型的Exchange：direct, topic 和fanout。fanout就是广播模式，会将所有的Message都放到它所知道的queue中。
创建一个名字为logs，类型为fanout的Exchange：
"""
channel.exchange_declare(exchange='direct_logs',
                         type='direct')
"""
消息要exchange到哪个queue,可以在consumer端定义,由于使用的是exchange使用的是fanout类型,只要是consumer端创建的queue都得到
productor发送的全部消息,意味着如果有多个consumer,那每个consumer都会得到相同的消息.而且这些队列在consumer关闭连接时就会被删除
"""
message = ' '.join(sys.argv[2:]) or "Hello World!"

channel.basic_publish(exchange='logs',
                      routing_key='',
                      body=message)
print "[x] sent %r:%r" %(message,)
connection.close()
