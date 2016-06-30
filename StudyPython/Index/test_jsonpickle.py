#!/usr/bin/env python
# coding:utf8

import jsonpickle
from datetime import datetime

class Contact:
    def __init__(self, **kargs):
        self.phone = kargs.setdefault('phone',None)
        self.email = kargs.setdefault('email',None)
    def convert(self):
        d = self.__dict__.copy()
        return d
    
class User:
    def __init__(self,**kargs):
        self.id = kargs.setdefault('id',None)
        self.name = kargs.setdefault('name',None)
        self.pwd = kargs.setdefault('pwd',None)
        self.ctime = kargs.setdefault('ctime',datetime.now())
        self.contact = kargs.setdefault('contact',None)
    def convert(self):
        d = self.__dict__.copy()
        d['ctime'] = self.ctime.strftime('%Y-%m-%d %H:%M:%S')
        d['contact'] = self.contact.convert()
        return d

u = User()
u.contact = Contact()
json = jsonpickle.encode(u)
print json
print jsonpickle.decode(json)
dir(u)