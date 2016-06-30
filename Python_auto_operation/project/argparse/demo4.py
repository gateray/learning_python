#!/usr/bin/env python
# coding: utf-8
# 选项的冲突处理conflict_handler

import argparse
"""
默认的conflict_handler,当某个选项出现两次就会抛出ArgumentError异常
"""
parser = argparse.ArgumentParser()
parser.add_argument('-f', '--foo', help='old foo help')
try:
    parser.add_argument('--foo', help='new foo help')
except argparse.ArgumentError as e:
    print("{}: argument --foo: conflicting option string(s): --foo".format(e.__class__.__name__))

"""
有时(例如使用parents从一个parser中继承选项参数)需要重写旧的使用相同选项字符串的参数,这时就可以使用'resolve'来解决选项冲突的问题
usage: demo4.py [-h] [-f FOO] [--foo FOO]

optional arguments:
  -h, --help  show this help message and exit
  -f FOO      old foo help
  --foo FOO   new foo help
"""
parser = argparse.ArgumentParser(conflict_handler='resolve')
parser.add_argument('-f', '--foo', help='old foo help')
parser.add_argument('--foo', help='new foo help')
parser.print_help()