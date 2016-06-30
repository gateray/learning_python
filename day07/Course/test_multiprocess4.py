#!/usr/bin/env python
# coding:utf8

from multiprocessing import Process
from multiprocessing import Pool

def foo(i):
    print 'hi'
    return i+100

def bar(arg):
    print arg
    print '-------------------'

pool = Pool(5)
pool.apply_async(func=foo,args=(1,),callback=bar)

