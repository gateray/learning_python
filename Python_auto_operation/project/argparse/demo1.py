#!/usr/bin/env python
# coding: utf-8

import argparse

#创建一个解析器
parser = argparse.ArgumentParser(description='Process some integers.')
"""
调用add_argument方法可以为ArgumentParser补全命令行参数的说明信息,告诉ArgumentParser怎样获取命令行的字符串参数并将其转换成相应的对象,
当调用parse_args方法时,这些信息被存储和使用.parse_args()的调用将会返回一个包含"integers"和"accumulate"属性的Namespace对象,integers属性是一
个包含一个或多个整数的list,accumulate属性会是sum()函数(--sum指定时)或者max()函数(--sum没指定时).
"""

parser.add_argument('integers', metavar='N', type=int, nargs='+',
                   help='an integer for the accumulator')
"""
nargs: 用于限定命令行选项或参数的出现次数
  '?': 0或1次
        >>> parser = argparse.ArgumentParser()
        >>> parser.add_argument('--foo', nargs='?', const='c', default='d')
        >>> parser.add_argument('bar', nargs='?', default='d')
        >>> parser.parse_args('XX --foo YY'.split())
        当选项或位置参数都出现1次时,--foo和bar都通过命令行参数传值
        Namespace(bar='XX', foo='YY')
        当命令行选项出现但没带参数值时, 选项对应的参数值为const关键字参数的值
        >>> parser.parse_args('XX --foo'.split())
        Namespace(bar='XX', foo='c')
        当命令行选项或参数都没出现时,都使用default关键字参数的值
        >>> parser.parse_args(''.split())
        Namespace(bar='d', foo='d')
  'n': n次
  '*': 0次或多次
        >>> parser = argparse.ArgumentParser()
        >>> parser.add_argument('--foo', nargs='*')
        >>> parser.add_argument('--bar', nargs='*')
        >>> parser.add_argument('baz', nargs='*')
        >>> parser.parse_args('a b --foo x y --bar 1 2'.split())
        Namespace(bar=['1', '2'], baz=['a', 'b'], foo=['x', 'y'])
  '+': 1次或多次
        >>> parser = argparse.ArgumentParser(prog='PROG')
        >>> parser.add_argument('foo', nargs='+')
        >>> parser.parse_args('a b'.split())
        Namespace(foo=['a', 'b'])
        >>> parser.parse_args(''.split())
        usage: PROG [-h] foo [foo ...]
        PROG: error: too few arguments
  'argparse.REMAINDER': 剩余的所有命令行参数或选项都应用到对应的选项或位置参数上
        >>> parser = argparse.ArgumentParser(prog='PROG')
        >>> parser.add_argument('--foo')
        >>> parser.add_argument('command')
        >>> parser.add_argument('args', nargs=argparse.REMAINDER)
        >>> print parser.parse_args('--foo B cmd --arg1 XX ZZ'.split())
        Namespace(args=['--arg1', 'XX', 'ZZ'], command='cmd', foo='B')

"""
parser.add_argument('--sum', dest='accumulate', action='store_const',
                   const=sum, default=max,
                   help='sum the integers (default: find the max)')
"""
dest='这里是目标的属性名,如果不指定默认为前面第一个参数所指定的选项或参数名称'
parse_args()会检查命令行,将每个参数转换为合适的类型,然后执行相应的动作
parser.parse_args(['--sum', '7', '-1', '42'])
Namespace(accumulate=<built-in function sum>, integers=[7, -1, 42])
如果调用parse_args()不传递参数列表时,会自动从命令行获取参数列表
"""
args = parser.parse_args()

print args.accumulate(args.integers)
