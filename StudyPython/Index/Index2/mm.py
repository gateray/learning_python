#!/usr/bin/env python
# coding:utf8

class Tree:
    @classmethod
    def method1(cls):
        pass
    @classmethod
    def method2(cls):
        Tree.method1()