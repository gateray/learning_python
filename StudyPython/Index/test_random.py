#!/usr/bin/env python
# coding:utf8

from random import randint, choice, randrange
from string import lowercase
from sys import maxint
from time import ctime

print randint(1,3)  #返回1-3中（包括3）的一个数字
print randrange(1,3) #返回1-3中（不包括3）的一个数字
print choice('seq')  #返回序列中的随机一个元素
print ctime(maxint)

doms = ('com','edu','net','org','gov')

for i in range(randint(5,10)):
    dtint = randint(0,maxint-1)
    ctime(dtint)
shorter = randint(4,7)
em = ''
for j in range(shorter):
    em += choice(lowercase)
longer = randint(shorter,12)
dn = ''
for j in range(longer):
    dn += choice(lowercase)

print '%s::%s@%s.%s::%d-%d-%d' % ('tom',em,dn,choice(doms),dtint,shorter,longer)