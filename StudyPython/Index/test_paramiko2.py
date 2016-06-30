#!/usr/bin/env python
# coding:utf8

import paramiko
import interactive

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('192.168.203.232', 22, 'root', 'redhat')

channel = ssh.invoke_shell()
interactive.interactive_shell(channel)
print '-'*100
channel.close()
ssh.close();
