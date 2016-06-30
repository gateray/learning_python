#!/usr/bin/env python
# coding:utf8
import pickle
import json
import os.path
from datetime import datetime,date
# from Index.test_json2obj import BeanFactory as bf
'''#pickle
d = dict(zip((1,2,3),[['zs','123'],['ls','123'],['ww','123']]))
with open('test.txt','w') as f:
    pickle.dump(d,f)
with open('test.txt','r') as f:
    print pickle.load(f)
'''
# d1 = {'zs':[1,2,3]}
# d2 = {'zs':[4,5,6]}
# with open('test.txt','a') as f:
#     pickle.dump(d1,f)
# with open('test.txt','a') as f:
#     pickle.dump(d2,f)
# 
# with open('test.txt','r') as f:
#     print pickle.load(f)

# d = dict(zip((1,2,3),(['zs','123'],['ls','123'])))
# d1 = None
# with open('test.txt','w') as f:
#     json.dump(d,f)
# with open('test.txt','r') as f:
#     d1 = json.load(f)
# print d1
# print 'zs' == d1['1'][0]
  
# print os.path.isfile('a.py')
# print os.path.isfile('b.py')
# 
class Contact:
    def __init__(self, **kargs):
        self.phone = kargs.setdefault('phone',None)
        self.email = kargs.setdefault('email',None)
    def convert(self):
        d = self.__dict__.copy()
        d['cls_name'] = str(self.__class__)
        return d
    
class User:
    def __init__(self,**kargs):
        self.id = kargs.setdefault('id',None)
        self.name = kargs.setdefault('name',None)
        self.pwd = kargs.setdefault('pwd',None)
        self.ctime = kargs.setdefault('ctime',None)
        self.contact = kargs.setdefault('contact',None)
        
    def convert(self):
        d = self.__dict__.copy()
        if type(self.ctime) is datetime:
            d['ctime'] = self.ctime.strftime('%Y-%m-%d %H:%M:%S')
        d['contact'] = self.contact.convert()
        d['cls_name'] = str(self.__class__)
        return d

u = User()
setattr(u, 'id',1)
setattr(u, 'name','user1')
setattr(u, 'pwd','user1')
setattr(u, 'ctime',datetime.now())
# setattr(u, 'contact',Contact(**{'phone':13588888888,'email':'aaa@aaa.com'}))
setattr(u, 'contact',Contact(phone=13588888888,email='aaa@aaa.com'))
user_json = json.dumps(u,default=u.__class__.convert)
print user_json
# print bf.json2obj(user_json).convert()
# print u.__class__
# print json.dumps({1:[1,2,3],2:4,3:date.today()})
# print vars(u)
# print type(getattr(u,'ctime'))
# print u.__module__,u.__class__
# 
# 
# li = [{1:1},[1,2,3]]
# print json.dumps(li)


# print json.loads('{ "keep_alive" : 125 }')