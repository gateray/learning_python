#!/usr/bin/env python
# coding:utf8
class Person:
    varname = 'notshared'
    __cname = '__cname'
    cname = 'cname'
    #构造方法
    def __init__(self,name):
        self.name = name
        #私有属性,外部不能访问
        self.__pri = 'xxx'
        print self
    def sth(self):
        print self
        print 'my name is %s' %self.name
        self.__getmoney()
    #私有方法，不能再外部调用
    def __getmoney(self):
        print self
        print 'call __getmoney(): this is a private method!'
    
    #类方法，与静态方法不一样的地方是它会自动接收一个类对象作为参数，由此可以方法类中的任何属性和方法    
    @classmethod
    def aaa(clz):
        print clz.__name__
        print clz.cname
        print clz.__cname
    #静态方法
    @staticmethod
    def bbb():
        print '--------->call bbb()'
        
    #特殊方法
    def __call__(self):
        print '叼你老母！'
    #析构方法
    def __del__(self):
        print 'bye' 

print '---------------创建p1,p2对象，调用构造方法---------------'
p1 = Person('laowang')
p2 = Person('laozhao')
print '-------------普通方法----------------'
p1.sth()
print '--------------测试对象属性---------------'
p1.varname = 1
p2.varname = 2
print '通过p1对象获取class中的varname：%s,p1对象中的varname: %s' %(p1.__class__.varname, p1.varname)
print 'p2对象中的varname：%s' % p2.varname
print 'Person类中的varname：%s' %Person.varname
print '--------------测试类方法--------------'
Person.aaa()
print '--------------测试静态方法-------------'
Person.bbb()
print '********class A(B,C): 这是多继承的写法，若B,C中含有相同的方法，则A默认继承第一个类（即：B）的方法*********'
print '------------特殊方法__call__(),如：p1 = Person(),执行p()时，将会调用Person类中的__call__()方法：'
p1()
print '--------------程序即将执行完毕，p1,p2对象即将释放时调用析构方法---------------'
#print Person.__cname
print Person.cname