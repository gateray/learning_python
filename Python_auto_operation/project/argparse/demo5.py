#!/usr/bin/env python
# coding: utf-8
# add_argument()参数详解

import argparse

parser = argparse.ArgumentParser(conflict_handler='resolve')
"""
add_argument(name or flags...[, action][, nargs][, const][, default][, type][, choices][, required][, help][, metavar][, dest])
name or flags - 可以是一个名称或者是选项列表字符串,如: 'foo'或 '-f' 或 '-f,--foo'.
action - 当参数在命令行出现时,便执行相应类型的action,action包含如下类型:
    'store': 默认类型,仅保存参数的值
    'store_const': 命令行参数或选项的值将保存为关键字参数const=value的值,即要求命令行选项后面不能跟随参数的时候使用
    'store_true'和'store_false': 是特殊的'store_const', 为命令行选项或参数的值将保存为True或False
    'append': 将命令行选项的参数值追加到一个list中, 用于命令行中多次使用同一选项的场景
    'append_const': 将关键字参数const=value的值作为命令行选项的参数值追加到一个list中
    'count': 用于计算命令行选项出现的次数, 一般用于实现增加详细级别输出的命令行选项
    'version': 当使用--version时,以关键字参数version=value的值作为--version的参数值,一般用于输出命令的版本信息
    '自定义action': 需要继承argparse.Action或实现相同的接口
nargs - 指定该选项支持的参数数量.
const - A constant value required by some action and nargs selections.
default - The value produced if the argument is absent from the command line.
type - The type to which the command-line argument should be converted.
choices - A container of the allowable values for the argument.
required - Whether or not the command-line option may be omitted (optionals only).
help - A brief description of what the argument does.
metavar - A name for the argument in usage messages.
dest - The name of the attribute to be added to the object returned by parse_args().
"""
print("---start test action store")
parser.add_argument('-f', '--foo')
ns = parser.parse_args(['-f', '/etc/passwd'])
print(ns)
print("---end---")

print("---start test action store_const---")
parser = argparse.ArgumentParser(conflict_handler='resolve')
parser.add_argument('-f', action='store_const', const='/etc/shadow')
# ns = parser.parse_args(['-f', '/etc/passwd'])这是错误的写法,正确写法如下:
ns = parser.parse_args(['-f'])
print(ns)
print("---end---")

print("---start test action store_true---")
parser = argparse.ArgumentParser(conflict_handler='resolve')
parser.add_argument('-f', action='store_true')
parser.add_argument('-g', action='store_false')
parser.add_argument('god', action='store_true')
parser.add_argument('hook')
ns = parser.parse_args(['-f', '-g','fuck'])
parser.print_help()
print(ns)
print("---end---")

print("---start test action append---")
parser = argparse.ArgumentParser(conflict_handler='resolve')
parser.add_argument('-f', action='append')
ns = parser.parse_args(['-f','/etc/passwd', '-f', '/etc/shadow'])
print(ns)
print("---end---")

print("---start test action append_const---")
parser = argparse.ArgumentParser()
parser.add_argument('--str', action='append_const', const=str)
parser.add_argument('--int', action='append_const', const=int)
parser.add_argument('-a', dest='types', action='append_const', const=1)
parser.add_argument('-b', dest='types', action='append_const', const=2)
ns = parser.parse_args('--str --int -a -b'.split())
print(ns)
print("---end---")

print("---start test action count---")
parser = argparse.ArgumentParser()
parser.add_argument('--verbose', '-v', action='count')
ns = parser.parse_args(['-vvv'])
print(ns)
print("---end---")

print("---start test action version---")
parser = argparse.ArgumentParser(prog='PROG')
parser.add_argument('-V','--version', action='version', version='%(prog)s 2.0')
try:
    print(parser.parse_args(['--version']))
except:
    pass
print("---end---")

print("---start test action 自定义action")
class FooAction(argparse.Action):
    def __init__(self, option_strings, dest, nargs=None, **kwargs):
        if nargs is not None:
            raise ValueError("nargs not allowed")
        super(FooAction, self).__init__(option_strings, dest, **kwargs)
    def __call__(self, parser, namespace, values, option_string=None):
        print '%r %r %r' % (namespace, values, option_string)
        setattr(namespace, self.dest, values)

parser = argparse.ArgumentParser()
parser.add_argument('--foo', action=FooAction)
parser.add_argument('bar', action=FooAction)
ns = parser.parse_args('1 --foo 2'.split())
print(ns)
print("---end---")