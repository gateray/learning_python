#!/usr/bin/env python
# coding: utf-8
# 对自定义对象进行排序

class Customize:
    def __init__(self, string, number, useNum=True):
        self.string = string
        self.number = number
        self.useNum = useNum

    def __lt__(self, other):
        if self.useNum:
            return self.number < other.number
        return self.string < other.string

    def __repr__(self):
        return "{}:{}".format(self.string, self.number)

if __name__ == '__main__':
    a = Customize('a', 4)
    b = Customize('b', 3)
    c = Customize('c', 2)
    d = Customize('d', 1)
    l = [a, b, c, d]
    print(l)
    l.sort()
    print(l)
    l.sort(key=lambda i: i.string)
    print(l)