#!/usr/bin/env python
# coding: utf8

from twisted.internet import protocol,reactor
from time import ctime

PORT = 21567

class TSServProtocol(protocol.Protocol):
    
    def connectionMade(self):
        clnt_addr = self.clnt = self.transport.getPeer().host
        print '...connected from: ', clnt_addr
    
    def dataReceived(self,data):
        self.transport.write('[%s] %s'%(ctime(),data))

factory = protocol.Factory()
factory.protocol = TSServProtocol
print 'waiting for connect...'
reactor.listenTCP(PORT,factory)
reactor.run()
