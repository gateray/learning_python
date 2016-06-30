#!/usr/bin/env python
# coding:utf8

import SocketServer

class MyTCPHandler(SocketServer.BaseRequestHandler):
    def __init__(self, request, client_address, server):
        SocketServer.BaseRequestHandler.__init__(self, request, client_address, server)
    
    def setup(self):
        SocketServer.BaseRequestHandler.setup(self)
        
    def handle(self):
#       while True:
            self.data = self.request.recv(1024).strip()
#            if not self.data: break
            print '{} wrote:'.format(self.client_address[0])
            print self.data
            self.request.sendall(self.data.upper())
    
    def finish(self):
        SocketServer.BaseRequestHandler.finish(self)

if __name__ == '__main__':
    HOST,PORT = 'localhost',9999
    server = SocketServer.ThreadingTCPServer((HOST,PORT),MyTCPHandler)
    server.serve_forever()