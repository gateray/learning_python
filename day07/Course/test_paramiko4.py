#!/usr/bin/env python
# coding:utf8

import os.path

import paramiko
'''使用公钥进行sftp认证'''
# #指定私钥文件路径
# private_key_path = os.path.expanduser('~/.ssh/id_rsa')
# #创建私钥对象
# key = paramiko.RSAKey.from_private_key_file(private_key_path)
#
# #创建传输对象
# t = paramiko.Transport(('192.168.203.232'),22)
# t.connect(username='root',pkey=key)
#
# sftp = paramiko.SFTPClient.from_transport(t)
# sftp.put('ks.cfg.58','/tmp/ks_from_remote')
#
# t.close()

private_key_path = os.path.expanduser('~/.ssh/id_rsa')
key = paramiko.RSAKey.from_private_key_file(private_key_path)

t = paramiko.Transport(('192.168.203.232',22))
t.connect(username='root',pkey=key)

sftp = paramiko.SFTPClient.from_transport(t)
sftp.get('/tmp/ks_from_remote','from_remote')
t.close()