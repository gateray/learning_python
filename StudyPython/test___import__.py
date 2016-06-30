#!/usr/bin/env python
# coding:utf8

#导入‘a.b.c’时，当fromlist为空（默认），获得的模块为‘a’，当fromlist不为空时（如下），获得的模块为‘a.b.c’
mod = __import__('Index.Index2.mm')
print dir(mod) 
# print getattr(mod, 'Index.Index2.mm.Tree')
_temp = __import__('Index.Index2.mm', fromlist=[''])
print dir(_temp)
print 'Index.Index2.mm.Tree'.split('.')[-1]