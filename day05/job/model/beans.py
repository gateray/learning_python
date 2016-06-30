#!/usr/bin/env python
# coding:utf8

class User:
    def __init__(self,**kargs):
        self.id = kargs.setdefault('id',None)
        self.name = kargs.setdefault('name',None)
        self.pwd = kargs.setdefault('pwd',None)
    def convert(self):
        d = self.__dict__.copy()
        d.update({'cls_name':str(self.__class__)})
        return d

class Message:
    def __init__(self,**kargs):
        self.id = kargs.setdefault('id',None)
        self.s_uid = kargs.setdefault('s_uid',None)
        self.r_uid = kargs.setdefault('r_uid',None)
        self.c_time = kargs.setdefault('c_time',None)
        self.content = kargs.setdefault('content',None)
    def convert(self):
        d = self.__dict__.copy()
        d['c_time'] = self.c_time.strftime('%Y-%m-%d %H:%M:%S')
        d['s_uid'] = self.s_uid.convert()
        d['r_uid'] = self.r_uid.convert()
        d.update({'cls_name':str(self.__class__)})
        return d

class QA:
    def __init__(self,**kargs):
        self.question = kargs.setdefault('question',None)
        self.answer = kargs.setdefault('answer',None)
    def convert(self):
        d = self.__dict__.copy()
        d.update({'cls_name':str(self.__class__)})
        return d

class Page:
    def __init__(self,**kargs):
        self.pgsize = 20 #page size
        self.allrecord = None  #sumary record count
        self.pgcount = None  #display record count per page
        self.cpgid = None  #current page number
        self.content = None  #content of page display
        self.frsize = 10  #frame size which include how many of page number
        self.frloffset = 5  #frame left offset
        self.lpgid = (self.cpgid-self.frloffset) if self.cpgid > self.frloffset else 1  #frame left page number
        self.rpgid = self.pgcount if (self.lpgid+self.frsize-1) >= self.pgcount else (self.lpgid+self.frsize-1)  #frame right page number
    def convert(self):
        d = self.__dict__.copy()
        d.update({'cls_name':str(self.__class__)})
        for i,obj in enumerate(d['content']):
            d['content'][i] = obj.convert()
        return d 
        
if __name__ == "__main__":
    print(User().convert())