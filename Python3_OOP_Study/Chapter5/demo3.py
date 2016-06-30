#!/usr/bin/env python
# coding: utf-8

class ReadOnlyX:
    def __setattr__(self, attr, value):
        if attr == 'x':
            raise AttributeError("X is immutable")
        super().__setattr__(attr, value)

    def __getattr__(self, attr):
        if attr == 'x':
            return 1
        super().__getattr__(attr)

class ReadOnlyY:
    def __getattribute__(self, attr):
        if attr == 'y':
            return "just try and change me!"
        return super().__getattribute__(attr)
    def __getattr__(self, attr):
        return 10


if __name__ == '__main__':
    rx = ReadOnlyX()
    print(rx.x)    #-> 1
    try:
        rx.x = 2
    except AttributeError as e:
        print(e.args[0])
    ry = ReadOnlyY()
    print(ry.y)    #-> just try and change me!
    ry.y='haha'
    print(ry.y)    #-> just try and change me!
    print(ry.z)    #-> 10