#!/usr/bin/env python
# coding:utf8
import hashlib

#md5
hash1 = hashlib.md5()
hash1.update('000000')
 
print hash1.hexdigest() 
def md5(pwd):
    hash = hashlib.md5()
    hash.update(pwd)
    return hash.hexdigest()
 
print len(md5('888888'))
