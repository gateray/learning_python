#!/usr/bin/env python
# coding:utf8
#

def mymap(func,seq):
    l = []
    for i in seq:
        l.append(func(i))
    return l

def func(i):
    return i**2

if __name__ == '__main__':
    print mymap(func,[1,2,3])
