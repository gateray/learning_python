#!/usr/bin/env python
# coding: utf8

import socket
#import ssl

sk = socket.socket()
#print type(socket.ssl(sk))
sk.connect(('192.168.124.147',9999))
while True:
    print sk.recv(1024)
    inp = raw_input('input: ').strip()
    sk.sendall(inp)
    if inp == '!': break
sk.close()