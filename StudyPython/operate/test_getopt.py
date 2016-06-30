#!/usr/bin/env python
# coding:Utf8

from getopt import getopt
import sys
#作用：获取命令行输入的命令选项（“-”短选项，“--”长选项）及参数
#getopt参数列表：arg1:命令行选项及参数列表；arg2：短选项字符串，若选项后面有":"表示该选项有选项值；
#arg3（可选）：长选项,若选项后面有"="表示有选项值
#返回值：optlist：由选项和选项值组成的元组的列表[(opt1,value1),(opt2,value2),...]
#参数：args：命令行选项后的参数列表
optlist, args = getopt(sys.argv[1:],
                'h?valqs:u:p:n:', ['help','h','?','ipv6','stddev='])
print optlist
print args

