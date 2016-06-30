#!/usr/bin/env python
# coding:utf8

#method1:
from multiprocessing import Process
# from multiprocessing import Array
#
# arr = Array('i',[11,22,33,44]) #'i'表示数组元素为int类型
#
# def foo(i):
#     arr[i] = 100+i
#     for item in arr:
#         print 'process: %d ---> item: %d' %(i,item)
#
# for i in range(2):
#     p = Process(target=foo,args=(i,))
#     p.start()
    # p.join()

#method2:
from multiprocessing import Manager
#
# manage = Manager()
# dic = manage.dict()
#
# def foo(i,dic):
#     dic[i] = 100 + i
#     print dic.values()
#
# for i in range(2):
#     p = Process(target=foo,args=(i,dic))
#     p.start()
#     p.join()

#method3:
manage = Manager()
namespace = manage.Namespace()
namespace.x = [11,22,33]

def foo(i,ns):
    namespace.x = i
    print namespace

for i in range(2):
    p = Process(target=foo,args=(i,namespace))
    p.start()
    p.join()
print namespace