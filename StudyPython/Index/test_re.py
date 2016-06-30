#!/usr/bin/env python
# coding:utf8

import re

print '---------高级应用----------'
p = re.compile (r'(?P<username>[^@:]*)(:?)(?P<password>.*)(?!\\)@(?P<hostname>[^:]*):?(?P<port>[0-9]*)')
mac =  p.search('root:root@127.0.0.1:3389::')
print mac.group()
print mac.groupdict()


print '---------测试match和search方法的区别-----------'
print re.match('a','ba')     #只有第一个字符匹配上，才有可能匹配成功，否则返回None.匹配到一个结果就马上返回
m = re.search('a','ba')   #只要字符串里有字符匹配上，就匹配成功，否则返回None.匹配到一个结果就马上返回
print m.group()          #不带参数的group将返回整个匹配到的字符串，带数字参数表示返回对应的分组匹配字符串


print '----------测试分组group()方法-----------'
regx = re.compile('(\w\w\w)-(\d\d\d)')
mach = regx.match('abc-123')
print 'group(): %s, group(1): %s, group(2): %s' %(mach.group(),mach.group(1),mach.group(2))


print '----------测试groups()方法------------'
m1 = re.match('a','abc')
m2 = re.match('(\w\w\w)-(\d\d\d)','ott-123')
print 'groups()只匹配分组，且返回的是一个元组'
print 'group(): %s, groups(): %r' %(m1.group(),m1.groups())
print m2.groups()


print '----------测试findall()方法-----------'
print '''
rs = re.findall('car', 'carry the barcardi to the car')
for s in rs:
    print s
'''
rs = re.findall('car', 'carry the barcardi to the car')
for s in rs:
    print s


print '-----------测试finditer()方法与group()或groups()方法的组合使用-------------'
print """
finditer()返回成功匹配的match对象的迭代器
rs = re.finditer('car', 'carry the barcardi to the car')
print rs
for s in rs:
    print s,'----------->',s.group()
"""
rs = re.finditer('car', 'carry the barcardi to the car')
print rs
for s in rs:
    print s,'----------->',s.group()

print """
匹配时忽略大小写
re.finditer('(th\w+) and (th\w+)','That and this',flags=re.I)
print rs1.next().groups()
"""
rs1 = re.finditer('(th\w+) and (th\w+)','That and this',flags=re.I)
print rs1.next().groups()


print '-----------测试sub()和subn()方法-----------'
print 'sub()用于替换匹配正则的字符串，返回替换后的字符串'
print '''
re.sub('X', 'Mr. Smith', 'attn: X\n\nDear X,\n')
'''
print re.sub('X','Mr. Smith','attn: X\n\nDear X,\n')
print '''
subn()用于替换匹配正则的字符串，返回一个替换后的字符串和被替换字符串数量组成的元组
re.subn('X', 'Mr. Smith', 'attn: X\n\nDear X,\n')
'''
print re.subn('X', 'Mr. Smith', 'attn: X\n\nDear X,\n')

print '-----------测试split()-------------'
print """
split()用于切割字符串，被正则匹配到的子字符串将作为字符串的分割符，切割成由多个子字符串组成的列表
$ who
wesley console Jun 20 20:33
wesley pts/9 Jun 22 01:38 (192.168.0.6)
wesley pts/1 Jun 20 20:33 (:0.0)
wesley pts/2 Jun 20 20:33 (:0.0)
wesley pts/4 Jun 20 20:33 (:0.0)
wesley pts/3 Jun 20 20:33 (:0.0)
wesley pts/5 Jun 20 20:33 (:0.0)
wesley pts/6 Jun 20 20:33 (:0.0)
wesley pts/7 Jun 20 20:33 (:0.0)
wesley pts/8 Jun 20 20:33 (:0.0)
"""
s = '''wesley console Jun 20 20:33
wesley pts/9 Jun 22 01:38 (192.168.0.6)
wesley pts/1 Jun 20 20:33 (:0.0)
wesley pts/2 Jun 20 20:33 (:0.0)
wesley pts/4 Jun 20 20:33 (:0.0)
wesley pts/3 Jun 20 20:33 (:0.0)
wesley pts/5 Jun 20 20:33 (:0.0)
wesley pts/6 Jun 20 20:33 (:0.0)
wesley pts/7 Jun 20 20:33 (:0.0)
wesley pts/8 Jun 20 20:33 (:0.0)'''
for line in s.split('\n'):
    print re.split(r'\s+',line)