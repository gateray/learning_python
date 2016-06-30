#!/usr/bin/env python
# coding: utf8

import socket
from time import ctime

HOST = ''
PORT = 21567
BUFSIZE = 1024
ADDR = (HOST,PORT)

ss = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
ss.bind(ADDR)
ss.listen(5)

while True:
    print 'waiting for connect...'
    cs,r_addr = ss.accept()
    print '...connected from: ', r_addr
    while True:
        data = cs.recv(BUFSIZE)
        if not data: break
        cs.send('[%s] %s' % (ctime(),data))
    cs.close()
ss.close()
