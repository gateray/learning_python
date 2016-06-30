#!/usr/bin/env python
# coding:utf8

import paramiko

#获取ssh客户端
ssh = paramiko.SSHClient()
#检查本地是否保存远程主机的密钥
if not ssh.load_system_host_keys():
    #如果本地未保存远程主机密钥，则自动添加
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
#连接远程主机
ssh.connect('192.168.203.232',username='root',password='redhat')
#执行命令，返回标准输入、输出、错误输出的文件IO对象
stdin,stdout,stderr = ssh.exec_command('cat /etc/passwd')
print 'cat /etc/passwd'
print '-'*100
#获取命令返回的输出结果
print stdout.read()
print 'end'
ssh.close()