#!/usr/bin/env python
#__*__coding:utf8__*__
#

f = open('test.txt','r')
for line in f.xreadlines():
    print line,
f.close()


with open('test.txt','r') as f:
    it = f.xreadlines()
    for line in it:
       print line, 
