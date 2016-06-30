#!/usr/bin/env python
# coding:utf8

from multiprocessing import Process
import threading
import time

def foo(i):
    print 'say hi',i

for i in range(10):
    p = Process(target=foo,args=(i,))
    p.start()

# for i in range(10):
#     t = threading.Thread(target=foo,args=(i,))
#     t.start()
