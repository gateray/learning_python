#!/usr/bin/env python
# coding:utf8

class Time60:
    def __init__(self,hr,mi):
        self.hr = hr
        self.mi = mi
        self.__hide = 'hide'
    def __str__(self):
        return '%s:%s' %(self.hr,self.mi)
    def __add__(self, other):
        return self.__class__((self.hr+other.hr),(self.mi+other.mi))
    def __iadd__(self, other):
        self.hr += other.hr
        self.mi += other.mi
        return self
    def __repr__(self):
        return "'" + self.__str__() +"'"

t1 = Time60(10,10)
t2 = Time60(12,20)
print t1,t2
print t1+t2
t1+=t2
print t1
print repr(t1)
#访问私有属性
print t1._Time60__hide
print '-'*200
import time
from random import choice

class RandSeq:
    def __init__(self,seq):
        self.data = seq
    def __iter__(self):
        return self
    def next(self):
        return choice(self.data)

it = RandSeq(('root','orchard','mysql'))
for i,elm in enumerate(it):
    if i == 3: break
    print elm
    time.sleep(1)
