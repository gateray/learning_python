#!/usr/bin/env python
# coding: utf-8

from random import choice
import string

'''
#python3中为string.ascii_letters,而python2下则可以使用string.letters和string.ascii_letters

def GenPassword(length=16,chars=string.ascii_letters+string.digits):
    return ''.join([choice(chars) for i in range(length)])

class Test:
    def __str__(self):
        return "this is a test"

if __name__=="__main__":
    #生成10个随机密码
    for i in range(10):
        #密码的长度为8
        print(GenPassword(8))

    print(Test())
'''

print("".join([ choice(string.ascii_letters+string.digits+"!@#$%^&") for len in range(16) ]))

from email.header import Header