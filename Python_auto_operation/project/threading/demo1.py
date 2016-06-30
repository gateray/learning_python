#!/usr/bin/env python
# coding: utf-8
# 线程局部变量

import threading
import time

tl = threading.local()

def exec_thread(name):
    tl.name = name
    use_localvar()

def use_localvar():
    for i in range(10):
        #直接引用线程局部变量
        print("thread: {0}, name: {1}".format(threading.currentThread().name, tl.name))
        time.sleep(1)

if __name__ == "__main__":
    t1 = threading.Thread(target=exec_thread,args=("tom",))
    t2 = threading.Thread(target=exec_thread,args=("jerry",))
    t1.setDaemon(True)    #当其他线程执行完毕后,该线程就要关闭
    t2.setDaemon(False)    #其他线程线程执行完毕后,该线程若没执行完则继续执行
    t1.start()
    t2.start()
    print("main-thread finished")


