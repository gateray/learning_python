#!/usr/bin/env python
# coding: utf-8

import curl

conn = curl.Curl()
print type(xrange(4))
print type(range(4))
for i in xrange(4):
    print i

a=1
b=2
def func():
    print "call func()"

locals()['func']()
print globals()
print locals()