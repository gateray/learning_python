#!/usr/bin/env python
# coding: utf-8
# 测试cStringIO

import cStringIO
"""
cStringIO,一个轻量级,更高效的StringIO,不支持unicode字符串作为输入.
与StringIO.StringIO('s')不同,cStringIO.StringIO('s')返回只读的对象(没有write方法)
"""
output = cStringIO.StringIO('aa')
# output.writelines('第一行.\n')
# output.writelines('second line.')
print >>output, 'bb'
print(output.getvalue())
output.close()
