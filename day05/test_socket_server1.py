#!/usr/bin/env python
# coding: utf8

import socket

# sk = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
sk = socket.socket()
addr = ('0.0.0.0',9999)
sk.bind(addr)
sk.listen(5)
while True:
    conn = None
    try:
        conn,r_addr = sk.accept()
        print 'connect by %s:%s' % (r_addr)
        conn.sendall('Welcome...')
        while True:
            data = conn.recv(1024)
            print '<--' + data
            if data == '!' or len(data) is 0: 
                break
            conn.sendall('sb')
    except KeyboardInterrupt:
        print '\n'
        exit()
    except Exception,e:
        print e
    finally:
        if conn is not None:
            print 'before close'
            conn.close()
