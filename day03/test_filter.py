#!/usr/bin/env python
# coding:utf8
#

def myfilter(func,seq):
    l = []
    for i in seq:
        elm = func(i)
        if elm:l.append(elm)
    return l

def func(elm):
    return elm if elm > 3 else None 

if __name__ == '__main__':
    print myfilter(func,[1,2,3,4,5])
