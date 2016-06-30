#!/usr/bin/env python
# coding:utf8

from ftplib import FTP
"""
不加密的ftp：
>>> from ftplib import FTP
>>> ftp = FTP('ftp.debian.org')     # connect to host, default port
>>> ftp.login()                     # user anonymous, passwd anonymous@
'230 Login successful.'
>>> ftp.cwd('debian')               # change into "debian" directory
>>> ftp.retrlines('LIST')           # list directory contents
-rw-rw-r--    1 1176     1176         1063 Jun 15 10:18 README
...
drwxr-sr-x    5 1176     1176         4096 Dec 19  2000 pool
drwxr-sr-x    4 1176     1176         4096 Nov 17  2008 project
drwxr-xr-x    3 1176     1176         4096 Oct 10  2012 tools
'226 Directory send OK.'
>>> ftp.retrbinary('RETR README', open('README', 'wb').write)
'226 Transfer complete.'
>>> ftp.quit()
"""

"""
加密的ftp
>>> from ftplib import FTP_TLS
>>> ftps = FTP_TLS('ftp.python.org')
>>> ftps.login()           # login anonymously before securing control channel
>>> ftps.prot_p()          # switch to secure data connection
>>> ftps.retrlines('LIST') # list directory content securely
total 9
drwxr-xr-x   8 root     wheel        1024 Jan  3  1994 .
drwxr-xr-x   8 root     wheel        1024 Jan  3  1994 ..
drwxr-xr-x   2 root     wheel        1024 Jan  3  1994 bin
drwxr-xr-x   2 root     wheel        1024 Jan  3  1994 etc
d-wxrwxr-x   2 ftp      wheel        1024 Sep  5 13:43 incoming
drwxr-xr-x   2 root     wheel        1024 Nov 17  1993 lib
drwxr-xr-x   6 1094     wheel        1024 Sep 13 19:07 pub
drwxr-xr-x   3 root     wheel        1024 Jan  3  1994 usr
-rw-r--r--   1 root     root          312 Aug  1  1994 welcome.msg
'226 Transfer complete.'
>>> ftps.quit()
>>>
"""
ftp = FTP('192.168.203.232')         #创建ftp连接对象
ftp.login(user='ftp',passwd='ftp')    #登陆ftp server
ftp.dir()            #列举所在远程目录下的所有文件
print ftp.pwd()      #显示当前所在的远程目录路径
ftp.cwd('ks')       #改变远程目录的路径，等同于cd
print ftp.pwd()
ftp.dir()
ftp.retrlines('RETR ks.cfg')
ftp.quit()

print '----------ftp下载文件正式的写法---------'
import ftplib
import os
import socket

HOST = '192.168.203.232'
DIRN = 'ks'
FILE = 'ks.cfg'

def main():
    try:
        f = ftplib.FTP(HOST)
    except (socket.error,socket.gaierror) as e:  #连接失败是会抛出socket.error,socket.gaierror异常
        print 'ERROR: cannot reach host %s' %HOST
        return
    print '*** Connected to host "%s" successful!' %HOST
    try:
        f.login()
    except ftplib.error_perm:  #登陆失败会抛出ftplib.error_perm异常
        print 'ERROR: cannot login anonymously'
        f.quit()
        return
    print '*** Logged in as "anonymous"'
    try:
        f.cwd(DIRN)
    except ftplib.error_perm: #若没有权限访问该目录，则抛出ftplib.error_perm异常
        print 'ERROR: cannot CD to "%s"' %DIRN
        f.quit()
        return
    print '*** Changed to "%s" folder' % DIRN
    try:
        f.retrlines('RETR %s' %FILE, open(FILE,'w').write)
    except ftplib.error_perm:    #若没有读取文件的权限则抛error_perm异常
        print 'ERROR: cannot read file "%s"' %FILE
        os.unlink(FILE)   #删除已打开的文件
    else:
        print '*** Downloaded "%s" to CWD' %FILE
    f.quit()
    return
if __name__ == '__main__':
    main()

print '----------测试上传文件----------'
HOST = '192.168.203.232'
FILE = 'ks.cfg'
def upload():
    try:
        ftp = FTP(HOST)
    except (socket.error,socket.gaierror) as e:
        print 'ERROR: 服务器不可达'
        return
    print 'connected to "%s" successful!' %HOST
    try:
        ftp.login()
    except ftplib.error_perm:
        print 'ERROR 不允许匿名登录'
        ftp.quit()
        return
    print '登录成功！'
    try:
        with open(FILE) as f:
            ftp.storlines('STOR %s' %FILE,f)
    except ftplib.error_perm:
        print 'ERROR: 权限问题'
    else:
        print '上传成功！'
    ftp.quit()
    return
if __name__ == '__main__':
    upload()