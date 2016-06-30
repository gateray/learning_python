#!/usr/bin/env python
# coding:utf8
import os.path as op
import os 

print '----------__file__-----------'
print __file__    #当前文件所在路径
print '----------abspath(path)------------'
print op.abspath('')
print '-----------altsep-------------'
print op.altsep   #自适应路径分隔符
print '-----------basename(path)--------------'
print op.basename('/a/b/c.txt')
print '------------dirname(path)-------------'
print op.dirname('/a/b/c.txt')
print '------------exists()--------------'
print op.exists('/a/b/c.txt')
print '------------op.expanduser(\'~\' or \'~administrator\')----'
print op.expanduser('~/a.txt')  #解析用户家目录符号
print '------------op.expandvars(环境变量名)------------'
print op.expandvars('$PATH')  #解析环境变量路径
print '------------扩展名分割符-----------'
print op.extsep
print '-------------getatime(path),getmtime(path),getctime(path)--------------'
print op.getatime('./a.py'), op.getctime('./a.py'), op.getmtime('./a.py')
print '------------getsize(path)------------'
print op.getsize('./a.py')
print '----------------isabs(path)------------'
print op.isabs('/b/b') #测试一个路径字符串是否为绝对路径
print '-------------isdir(path),isfile(path),islink(path),ismount(path)'
print op.isdir('.'), op.isfile('./a.py'), op.islink('./a.py'), op.ismount('./a.py')
print '--------------realpath(path)-----------'
print op.realpath('a.py') #传递一个相对路径返回一个绝对路径
print '-----------split(path)----------'
print op.split('/a/b/c.txt') #分割路径和文件
print '-----------splitext--------'
print op.splitext('/a/b/c.txt')  #分割路径和扩展名
print '------------join(path1,path2,...)--------'
print op.join(op.dirname(__file__),'b','c.txt') #合并路径
print '------------walk(path)------------'
for x,y,z in os.walk('H:/PycharmProjects'):
    print 'root: %s, dirs: %r, files: %r'%(x,y,z)

print '------------os.stat()--------------'
print os.stat('test.txt').st_size




        