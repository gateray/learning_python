#!/usr/bin/env python
# coding:utf8

import socket
ADDR = ('127.0.0.1',9999)
ss = socket.socket()
ss.bind(ADDR)
ss.listen(5)
try:
    while True:
        conn,addr = ss.accept()
        while True:
            data = conn.recv(2)
            if not data:break
            print data
        print 'before close()'
        conn.close()
except KeyboardInterrupt:
    ss.close()

