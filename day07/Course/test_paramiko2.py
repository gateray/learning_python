#!/usr/bin/env python
# coding:utf8

import os,sys

import paramiko
'''上传下载文件'''
# t = paramiko.Transport(('192.168.203.232',22))
# t.connect(username='root',password='redhat')
# sftp = paramiko.SFTPClient.from_transport(t)
'''put(localpath,remotepath)'''
# sftp.put('__init__.py','/tmp/__init__.py')
# t.close()

#创建Transport对象
t = paramiko.Transport(('192.168.203.232',22))
#连接远程主机
t.connect(username='root',password='redhat')
#从Transport对象中获取sftp客户端对象
sftp = paramiko.SFTPClient.from_transport(t)
#执行sftp命令
#get(remotepath,localpath)
sftp.get('/root/ks.cfg.58','ks.cfg.58')
t.close()