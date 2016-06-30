#!/usr/bin/env python
# coding:utf8
from abc import abstractmethod, ABCMeta


print '-------------测试抽象类，含有抽象方法的类就叫抽象类,抽象类不能被实例化-----------'
class AbsClass:
    __metaclass__ = ABCMeta
    @abstractmethod
    def get(self):
        print 'this is a abstractmethod'
    @abstractmethod
    def set(self):
        print 'this is another absmethod'
print '-----------使用抽象类的特性来定义规范，约束子类----------'
print '-----------子类继承了抽象类，必须要将其抽象方法重新实现，否则会报错--------------'
class SubClass(AbsClass):
    def get(self):
        AbsClass.get(self)
        print 'overide get() method'
    def set(self):
        print 'overide set() method'
SubClass().get()
SubClass().set()