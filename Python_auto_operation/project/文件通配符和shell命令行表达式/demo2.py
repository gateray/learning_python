#!/usr/bin/env python
# coding: utf-8

import fnmatch

#测试一个文件名是否匹配通配符表达式
print fnmatch.fnmatch('101.txt','*.txt')          #True
print fnmatch.fnmatch('101.txt','[!2-9]*.txt')    #True
print fnmatch.fnmatch('101.txt','[2-9]*.txt')     #False
print fnmatch.fnmatch('101.txt', '[0-9]*.txt')    #True

#从一个路径列表中,帅选出匹配通配符表达式的路径
print fnmatch.filter('1.py 2.txt 3.txt 4.c'.split(), '*.txt')