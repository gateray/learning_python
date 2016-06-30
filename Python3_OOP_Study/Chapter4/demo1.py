#!/usr/bin/env python
# coding: utf-8

class EvenOnly(list):
    def append(self, integer):
        if not isinstance(integer, int):
            raise TypeError("Only integers can be added")
        if integer % 2:
            raise ValueError("Only even numbers can be added")
        super().append(integer)

if __name__ == '__main__':
    evenli = EvenOnly()
    try:
        evenli.append("a")
    except TypeError as e:
        print("[{}] {}".format(e.__class__.__name__, e.args[0]))
    try:
        evenli.append(1)
    except ValueError as e:
        print("[{}] {}".format(e.__class__.__name__, e.args[0]))
    evenli.append(2)
    print(evenli[-1])