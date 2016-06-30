#!/usr/bin/env python
# coding:utf8

import os
import sys


f_r = os.popen('uname -a')  #默认以读模式打开一个命令的输出管道，read管道时将返回命令的输出结果
data = f_r.read()
f_r.close()
print data

f_w = os.popen("tr 'a-z' 'A-Z'",'w')  #以写的模式打开一个命令的输入管道，往该管道写的数据将作为命令的输入，关闭管道时，返回命令执行结果
print '-'*50
f_w.write('hello world')
print '-'*50
f_w.close()
print '-'*50


i,o = os.popen2("tr 'a-z' 'A-Z'")  #执行一个命令并返回该命令的管道(文件)输入端和输出端，输入端可以写入数据，用于命令接收，输出端可以读取数据，用于命令返回结果
i.write('fuck')
i.close()
print o.read()
o.close()

print '------------------以上方法在python2.6以后已经被废弃，使用subprocess模块中的方法来替代-----------------'
print '=====这行shell命令====='
import subprocess
output = subprocess.check_output(['ls','-l','/etc/motd'])  #执行shell命令，传递一个列表参数，列表首元素为命令，后面元素为命令选项或参数,返回命令执行结果
print output
print '=====执行管道命令====='
"""
output=`dmesg | grep init`
# becomes
p1 = Popen(["dmesg"], stdout=PIPE)
p2 = Popen(["grep", "init"], stdin=p1.stdout, stdout=PIPE)
p1.stdout.close()  # The p1.stdout.close() call after starting the p2 is important in order for p1 to receive a SIGPIPE if p2 exits before p1.
output = p2.communicate()[0]
"""
p1 = subprocess.Popen(['dmesg'], stdout=subprocess.PIPE)
p2 = subprocess.Popen(['grep','init'],stdin=p1.stdout,stdout=subprocess.PIPE)
p1.stdout.close()
print p2.communicate()[0] #等于stdout.read(),并自动close文件
# print p2.stdout.read()
# p2.stdout.close()

print '=====os.system()的替代====='
status = subprocess.call('ls -l /etc/passwd',shell=True) #输出命令执行结果并返回状态码
print status
print '=====实际应用中的标准写法====='
try:
    retcode = subprocess.call('ls -l /etc/passwd',shell=True)
    if retcode < 0:
        print >> sys.stderr, 'Child was terminated by sinal', -retcode
    else:
        print >> sys.stderr, 'Child returned', retcode
except OSError as e:
    print >> sys.stderr, 'Execution failed:',e

print '=====os.spawn()的替代====='
pid1 = os.spawnlp(os.P_NOWAIT,'/bin/ls','ls','-l','/etc/passwd') #返回子进程id
pid2 = subprocess.Popen(['/bin/ls','-l','/etc/passwd']).pid
print pid1,pid2
print subprocess.call(['/bin/ls','/etc/passwd']) #等同于os.spawnlp(os.P_WAIT,'/bin/ls','/etc/passwd'),返回执行状态码

print '=====替代os.popen*()====='
print '''
[os.popen()](读模式)
pipe = os.popen("cmd", 'r', bufsize)
==>
pipe = Popen("cmd", shell=True, bufsize=bufsize, stdout=PIPE).stdout
------------------------------------------------------------------------------
[os.popen()](写模式)
pipe = os.popen("cmd", 'w', bufsize)
==>
pipe = Popen("cmd", shell=True, bufsize=bufsize, stdin=PIPE).stdin
------------------------------------------------------------------------------
[os.popen2()]
(child_stdin, child_stdout) = os.popen2("cmd", mode, bufsize)
==>
p = Popen("cmd", shell=True, bufsize=bufsize,
          stdin=PIPE, stdout=PIPE, close_fds=True)
(child_stdin, child_stdout) = (p.stdin, p.stdout)
------------------------------------------------------------------------------
[os.popen3()]
(child_stdin,
 child_stdout,
 child_stderr) = os.popen3("cmd", mode, bufsize)
==>
p = Popen("cmd", shell=True, bufsize=bufsize,
          stdin=PIPE, stdout=PIPE, stderr=PIPE, close_fds=True)
(child_stdin,
 child_stdout,
 child_stderr) = (p.stdin, p.stdout, p.stderr)
 -----------------------------------------------------------------------------

'''
print type(subprocess.PIPE)
subprocess.call('date +%Y-%m-%d',shell=True)
