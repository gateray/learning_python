#!/usr/bin/env python
# coding: utf-8
# 选项的前缀字符

import argparse
"""
prefix_chars用来定义选项字符串的前缀,默认是'-'
"""
parser = argparse.ArgumentParser(prefix_chars='-+')
#这里的'+f'表示短选项
parser.add_argument('+f')
#这里的'++bar'表示长选项
parser.add_argument('++bar')
ns = parser.parse_args(['+f', 'X', '++bar', 'y'])
print(ns)


with open('args.txt','w') as fp:
    fp.write('-b\nbar\n-c\nxxx.conf')
#fromfile_prefix_chars定义一个参数的前缀字符,表示从文件里获取命令选项和参数
parser = argparse.ArgumentParser(fromfile_prefix_chars='@')
parser.add_argument('-b')
parser.add_argument('-c')
ns = parser.parse_args(['@args.txt'])
print(ns)