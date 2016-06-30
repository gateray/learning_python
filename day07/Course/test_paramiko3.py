#!/usr/bin/env python
# coding:utf8

import os.path

import paramiko

'''使用公钥进行ssh的认证'''
#指定私钥文件路径
private_key_path = os.path.expanduser('~/.ssh/id_rsa')
#根据私钥文件的路径创建私钥对象
key = paramiko.RSAKey.from_private_key_file(private_key_path)
#获取ssh客户端
ssh = paramiko.SSHClient()
#检查本地是否保存远程主机密钥
if not ssh.load_system_host_keys():
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
#连接远程主机
ssh.connect('192.168.203.232',username='root',pkey=key)

stdin,stdout,stderr = ssh.exec_command('df -h')
print stdout.read()
ssh.close()