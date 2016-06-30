#!/usr/bin/env python
# coding:utf8

print '\n'.join([' '.join(['%d*%d=%d' %(x,y,x*y) for x in range(1,y+1)]) for y in range(1,10)])

print '\n'.join([' '.join(['%d * %d = %d' %(j,i,j*i) for j in range(1,i+1)]) for i in range(1,10)])