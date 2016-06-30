#!/usr/bin/env python
# coding: utf-8

from IPy import IP

#获取ip地址协议版本
ipversion = IP('10.1.1.1').version()
if ipversion == 4: print("ipv4")

#获取指定ip网段下的ip个数(包含广播地址和网络地址)
print(IP('192.168.1.0/24').len())     #->256

#获取指定网段下的有效ip列表
ips = IP('192.168.1.0/24')
available_ips = [ ip[1] for ip in enumerate(ips) if ip[0] != 0 and ip[0] != ips.len()-1 ]
for ip in available_ips:
    print(ip)

#获取反向地址格式:
ip = IP('192.168.1.20')
print(ip.reverseName())        # -> 20.1.168.192.in-addr.arpa.
#获取ip地址是公网还是私网
print(ip.iptype())                    # -> PRIVATE
#根据ip和掩码生成网段格式
print(ip.make_net('255.255.255.0'))    # -> 192.168.1.0/24

#判断一个ip是否在一个网段中
ip = '192.168.1.20'
print(ip in IP('192.168.1.0/24'))     #-> True

#判断一个网段是否为另一个网段的子网
print(IP("192.168.1.0/24") in IP("192.168.0.0/16"))     #-> True
