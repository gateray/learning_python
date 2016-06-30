#!/usr/bin/env python
# coding: utf8

import socket

HOST = 'localhost'
PORT = 21567
BUFSIZE = 1024
ADDR = (HOST,PORT)

cs = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
cs.connect(ADDR)

while True:
    data = raw_input('> ')
    if not data:
        break
    cs.send(data)
    data = cs.recv(BUFSIZE)
    if not data:
        break
    print data
cs.close()
