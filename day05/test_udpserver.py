#!/usr/bin/env python
# coding: utf8

import socket
from time import ctime

HOST = ''
PORT = 21567
BUFSIZE = 1024
ADDR = (HOST,PORT)

ss = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
ss.bind(ADDR)
try:
    while True:
        print 'waiting for message...'
        data, r_addr = ss.recvfrom(BUFSIZE)
        ss.sendto('[%s] %s' %(ctime(),data),r_addr)
        print '...received from and returned to:', r_addr
except KeyboardInterrupt:
    ss.close()
