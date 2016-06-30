#!/usr/bin/env python
# coding:utf8

import socket
#import sys

HOST,PORT = 'localhost',9999
#data = ''.join(sys.argv[1:])


sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
sock.connect((HOST,PORT))
while True:
    data = raw_input('> ')
    if not data: break
    sock.sendall(data)
    data = sock.recv(1024)
    if not data: 
        print 'server is close()'
        break
    print data.strip()
sock.close()
    
