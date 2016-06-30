#!/usr/bin/env python
# coding: utf-8

def test():
    print("break1")
    yield 1
    print("break2")
    yield 2
    print("break3")
    yield 3
    print("break4")
    yield 4

obj = test()

obj.__next__()
obj.__next__()
obj.__next__()
obj.__next__()
