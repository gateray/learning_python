#!/usr/bin/env python
# coding:utf8
'''
功能：
    atexit.register(func)在程序退出时进行函数func回调，因此可以用于资源回收
'''
#1.测试不带参数的func
# try:
#     _count = int(open("counter").read())
# except IOError:
#     _count = 0
#
# def incrcounter(n):
#     global _count
#     _count = _count + n
#
# def savecounter():
#     open("counter", "w").write("%d" % _count)
#
# import atexit
# atexit.register(savecounter)
# incrcounter(1)

#2 测试带参数的func,栈结构，退出时后注册的func先被调用
# def goodbye(name, adjective):
#     print 'Goodbye, %s, it was %s to meet you.' % (name, adjective)
#
# import atexit
# atexit.register(goodbye, 'Donny', 'nice')
# # or:
# atexit.register(goodbye, adjective='nice', name='Danfi')

#3 作为装饰器来使用，被装饰的函数在程序退出时调用
import atexit

@atexit.register
def goodbye():
    print "You are now leaving the Python sector."


