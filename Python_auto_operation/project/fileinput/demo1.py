#!/usr/bin/env python
# coding: utf-8

import fileinput

"""
典型的用法:
for line in fileinput.input(files=None, inplace=0, backup="", bufsize=0,
          mode="r", openhook=None):
    process(line)
使用场景:
要对多个文件进行读写时使用,若对单个文件进行读写只需使用open()
使用详解:
input()实际是FileInput类的一个工厂方法,调用则返回一个FileInput对象,FileInput对象是一个可迭代对象.
FileInput对象迭代时,先从sys.argv[1:]获取文件名称列表,如果sys.argv[1:]为空,则从标准输入获取文件名称.如果
文件名为'-',也表示从标准输入获取文件名称,也可以手动传递一个文件名称的list,这些文件名称列表都会作为input()的第一个参数传递.
每次迭代都将返回当前文件的一行内容,当迭代完当前文件最后一行时,会将下一个文件指向当前文件,直到迭代到最后一个文件的最后一行时,迭代才终止.
迭代过程中,所有的sys.stdout都会转换为当前的文件对象.
inplace=1,表示先对当前文件进行备份.
backup='.bak',表示指定备份文件的后缀名,默认为.bak
openhook=hook_compressed, openhook关键字参数可以指定一个打开文件前的回调函数,该回调函数必须传递(filename, mode)两个参数
hook_compressed是fileinput模块自带的钩子函数,可以打开gz和bz2压缩的文件
"""