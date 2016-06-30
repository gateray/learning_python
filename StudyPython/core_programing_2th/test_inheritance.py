#!/usr/bin/env python
# coding:utf8

class RoundFloat(float):
    def __new__(cls, val):
        return float.__new__(cls,round(val,2))

rf = RoundFloat(1.666)
print rf , type(rf)

class RoundFloat2(float):
    def __new__(cls,val):
        return super(RoundFloat2,cls).__new__(cls,round(val,2))

rf2 = RoundFloat2(1.6666)
print rf2, type(rf2)

#派生可变类型子类
class SortedKeyDict(dict):
    def keys(self):
        return sorted(super(SortedKeyDict,self).keys())

d = SortedKeyDict((('abc',1),('abz',2),('cbd',3)))
print d.keys()

