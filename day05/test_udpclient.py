#!/usr/bin/env python
# coding: utf8

import socket

HOST = 'localhost'
PORT = 21567
BUFSIZE = 1024
ADDR = (HOST,PORT)

cs = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
#print cs.settimeout(3)
while True:
    data = raw_input('> ')
    if data == '!': break
    cs.sendto(data,ADDR)
    print '-->'+data
    data, s_addr = cs.recvfrom(BUFSIZE)
    print '<--'+data
    if not data: break
cs.close()
    
