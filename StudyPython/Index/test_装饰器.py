#!/usr/bin/env python
# coding:utf8
'''带参数的装饰器
def deco(arg):
    def _deco(func):
        def __deco():
            print("before %s called [%s]." % (func.__name__, arg))
            func()
            print("  after %s called [%s]." % (func.__name__, arg))
        return __deco
    return _deco

#带参数的装饰器，存在三层函数调用，第一层调用传递的是装饰器参数，调用结果返回第二层函数对象，该对象接受被装饰函数对象作为形参，然后被调用返回第三
#层函数对象，该函数对象接收被装饰函数的所有参数作为形参 
@deco("mymodule")
def myfunc():
    print(" myfunc() called.")
 
@deco("module2")
def myfunc2():
    print(" myfunc2() called.")
 
myfunc()
myfunc2()
'''
from test.inspect_fodder2 import wrap

'''让装饰器带类参数
class locker:
    def __init__(self):
        print("locker.__init__() should be not called.")
         
    @staticmethod
    def acquire():
        print("locker.acquire() called.（这是静态方法）")
         
    @staticmethod
    def release():
        print("  locker.release() called.（不需要对象实例）")
 
def deco(cls):
    #cls 必须实现acquire和release静态方法
    def _deco(func):
        def __deco():
            print("before %s called [%s]." % (func.__name__, cls))
            cls.acquire()
            try:
                return func()
            finally:
                cls.release()
        return __deco
    return _deco
 
@deco(locker)
def myfunc():
    print(" myfunc() called.")
myfunc()'''

'''装饰器带类参数，并对一个函数应用多个装饰器'''
class mylocker:
    def __init__(self):
        print("mylocker.__init__() called.")
         
    @staticmethod
    def acquire():
        print("mylocker.acquire() called.")
         
    @staticmethod
    def unlock():
        print("  mylocker.unlock() called.")
 
class lockerex(mylocker):
    @staticmethod
    def acquire():
        print("lockerex.acquire() called.")
         
    @staticmethod
    def unlock():
        print("  lockerex.unlock() called.")
 
def lockhelper(cls):
    #cls 必须实现acquire和release静态方法
    def _deco(func):
        @wrap(func)
        def __deco(*args, **kwargs):
            print("before %s called." % func.__name__)
            cls.acquire()
            try:
                return func(*args, **kwargs)
            finally:
                cls.unlock()
        return __deco

class example:
#     @lockhelper(mylocker)
#     def myfunc(self):
#         print(" myfunc() called.")
#  
    @lockhelper(mylocker)
    @lockhelper(lockerex)
    def myfunc2(self, a, b):
        print(" myfunc2() called.")
        return a + b
 
if __name__=="__main__":
    a = example()
#     a.myfunc()
#     print(a.myfunc())
    print(a.myfunc2(1, 2))
#     print(a.myfunc2(3, 4))
