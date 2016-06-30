#!/usr/bin/env python
# coding: utf-8

class Silly:
    @property
    def silly(self):
        "This is a silly property"
        print("you are getting silly")
        return self._silly
    @silly.setter
    def silly(self, value):
        print("you are making silly {}".format(value))
        self._silly = value
    @silly.deleter
    def silly(self):
        print("whoah, you killed silly!")
        del self._silly

if __name__ == '__main__':
    s = Silly()
    s.silly = 'haha'
    print(s.silly)
    del(s.silly)
    try:
        print(s.silly)
    except AttributeError:
        print("over")