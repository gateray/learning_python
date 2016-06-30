#!/usr/bin/env python
# coding:utf8

import threading
import sys

import paramiko

#获取ssh客户端
ssh = paramiko.SSHClient()
#检查本地是否保存远程主机的密钥
if not ssh.load_system_host_keys():
    #如果本地未保存远程主机密钥，则自动添加
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
#连接远程主机
ssh.connect('192.168.203.232',username='root',password='redhat')
print '1-------------------------------------'
channel = ssh.invoke_shell()
print '2-------------------------------------'
#count = 0
def get():
    #global count
    while True:
        res = channel.recv(256)
        #count += 1
        #print str(count)
        if not res:
            break
        sys.stdout.write(res)
        sys.stdout.flush()
t = threading.Thread(target=get)
t.start()
print '3-------------------------------------'
while True:
    data = sys.stdin.read(1)  #sys.stdin.read(1)一开始为阻塞态，等待一个字符串的标准输入（以回车结束），然后从标准输入缓冲区中逐字节读取出来然后赋值给data，直到标准输入缓冲区中没有数据为止（读完回车符），这时又回到阻塞态
    #print 'finish input'
    channel.send(data)

print '4-------------------------------------'
# channel.sendall('df -h')
# res = channel.recv(1024)
# print res
print '5-------------------------------------'
