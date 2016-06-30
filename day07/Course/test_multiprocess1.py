#!/usr/bin/env python
# coding:utf8

from multiprocessing import Process
import time

def say(i):
    print 'say hi',i

for i in range(10):
    p = Process(target=say,args=(i,))
    p.start()
