#!/usr/bin/env python
# coding: utf-8
# 测试StringIO

import StringIO

"""
以file-like的方式读写string(即stringbuffer:内存文件)
支持unicode和8bit字符串作为输入源
"""
output = StringIO.StringIO('中文')
print(output.getvalue())
print("-------------------------")
output.write('first line.\n')
#将'second line.'追加到output对象中
output.writelines('第二行数据.')
print >>output, "\n第三行数据."
print(output.getvalue())
output.close()
