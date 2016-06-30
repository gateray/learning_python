#!/usr/bin/env python
# coding: utf-8
# 测试ns对象的返回值

import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--foo', help='foo help')
#执行时如果不指定--foo,则返回foo=None,指定了--foo则后面必须跟一个选项的参数(只能跟一个,多于一个会报错),不跟则会报错
ns = parser.parse_args()
print(ns)
