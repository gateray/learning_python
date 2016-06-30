#!/usr/bin/env python
# coding: utf-8

import psutil
from datetime import datetime

#获取内存总量,使用量等信息(单位:byte)
"""
total: 16388935680, used: 5334380544
"""
mem = psutil.virtual_memory()
print("total: {}, used: {}".format(mem.total, mem.used))

#获取系统范围的cpu时间(单位秒)
"""
cpuid:0, user:917.86, nice:32.48, system:394.01, idle:17365.95, iowait:7.76, irq:0.0, softirq:4.9, steal:0.0, guest:0.0, guest_nice:0.0
cpuid:1, user:598.33, nice:24.53, system:212.18, idle:17983.31, iowait:6.35, irq:0.0, softirq:0.05, steal:0.0, guest:0.0, guest_nice:0.0
cpuid:2, user:879.8, nice:30.59, system:387.73, idle:17430.78, iowait:6.21, irq:0.0, softirq:2.47, steal:0.0, guest:0.0, guest_nice:0.0
cpuid:3, user:521.86, nice:20.51, system:228.57, idle:18049.43, iowait:5.95, irq:0.0, softirq:0.22, steal:0.0, guest:0.0, guest_nice:0.0
cpuid:4, user:880.48, nice:31.6, system:369.19, idle:17448.3, iowait:6.59, irq:0.0, softirq:2.02, steal:0.0, guest:0.0, guest_nice:0.0
cpuid:5, user:618.67, nice:27.88, system:218.86, idle:17950.53, iowait:5.14, irq:0.0, softirq:0.36, steal:0.0, guest:0.0, guest_nice:0.0
cpuid:6, user:908.31, nice:32.92, system:369.22, idle:17423.71, iowait:7.14, irq:0.0, softirq:2.3, steal:0.0, guest:0.0, guest_nice:0.0
cpuid:7, user:636.5, nice:26.95, system:225.23, idle:17924.24, iowait:9.92, irq:0.0, softirq:0.24, steal:0.0, guest:0.0, guest_nice:0.0

"""
cputimes_list = psutil.cpu_times(percpu=True)
for id,cputimes in enumerate(cputimes_list):
    print("cpuid:{0}, user:{user}, nice:{nice}, system:{system}, idle:{idle}, "
          "iowait:{iowait}, irq:{irq}, softirq:{softirq}, steal:{steal}, guest:{guest},"
          " guest_nice:{guest_nice}".format(id,**cputimes.__dict__))

#获取交换内存swap信息
swapinfo = psutil.swap_memory()
print(swapinfo)

#获取磁盘信息
partition_list = psutil.disk_partitions()
print(partition_list)
#获取/分区的磁盘使用率
partition_usage = psutil.disk_usage('/')
print(partition_usage)
#获取磁盘io信息
partition_io = psutil.disk_io_counters(perdisk=True)
print(partition_io)

#获取网络信息
net_io = psutil.net_io_counters(pernic=True)
print(net_io['eth0'])

#获取当前连接用户登录
current_user_info = psutil.users()
print(current_user_info)

#获取系统开机时间
boottime = psutil.boot_time()
print(datetime.fromtimestamp(boottime).strftime("%Y-%m-%d %H:%M:%S"))
