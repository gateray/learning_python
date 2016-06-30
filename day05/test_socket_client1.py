#!/usr/bin/env python
# coding: utf8

import socket
import time

sk = socket.socket()
sk.connect(('127.0.0.1',9999))
while True:
    print sk.recv(1024)
    inp = raw_input('input: ').strip() 
    inp = '\n' if len(inp) is 0 else inp
    if inp == '!': 
        break
    sk.sendall(inp)
sk.close()
