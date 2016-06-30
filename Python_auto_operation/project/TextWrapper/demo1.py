#!/usr/bin/env python
# coding: utf-8
# dedent提供了除去代码块中文本缩进的功能

from textwrap import dedent
def test():
    s = '''\
    hello
        world
    '''
    print(s)
    print(dedent(s))

if __name__ == '__main__':
    test()
