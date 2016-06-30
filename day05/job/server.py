#!/usr/bin/env python
# coding:utf8

import SocketServer
import util

class MyRequestHandler(SocketServer.BaseRequestHandler):
        
    def setup(self):
        self.user = None
    
    def handle(self):
        cs = self.request
        while True:
            cs.recv(1024)  

    def finish(self):
        self.user = None


if __name__ == '__main__':
    addr = (util.loadconfig()['socketconfig']['LISTENIP'], util.loadconfig()['socketconfig']['PORT'])
    server = SocketServer.ThreadingTCPServer(addr,MyRequestHandler)
    server.serve_forever()
