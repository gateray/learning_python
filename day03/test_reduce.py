#!/usr/bin/env python
#

def myreduce(func,seq,orig=0):
    for i in seq:
        orig = func(orig,i)
    return orig
        
def func(orig,i):
    return orig+i

if __name__ == '__main__':
    print myreduce(func,[1,2,3],10)
