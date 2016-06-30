#!/usr/bin/env python
# coding:utf8

i = 2
def haha():
    print "---"

print eval('lambda k:k**3')(3)
# print globals()
exec('a=lambda k:k**2;print(a(i))',globals())

#compile('code','','type') type include:'eval','single','exec'
print '-----------type "eval"------------'
eval_code = compile('x+y','','eval')
print eval(eval_code,{'x':1,'y':1})
print '-----------type "single"------------'
single_code = compile('print "%d+%d=%d"%(x,y,x+y)','','single')
exec(single_code,{'x':1,'y':1})
print '-----------type "exec"-------------'
exec_code = compile('''
for i in range(j):
    print i
print "end for"
''','','exec')
exec(exec_code,{'j':3})

#从文件对象执行代码
print '--------test exec fileobj---------- '
fobj = open('xcount.py')
exec fobj
fobj.seek(0)
exec fobj
fobj.close()
# exec fobj
"""
execfile(filename)等同于
fobj = open(filename,'r')
exec fobj
fobj.close()
"""