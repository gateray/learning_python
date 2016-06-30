#!/usr/bin/env python
# coding: utf-8

import os
import json
import sys
from pymongo import MongoClient

class MongoAPI:
    def __init__(self,host="localhost",port=27017,db="admin",username=None,pwd=None):
        self.host = host
        self.port = port
        self.db = db
        self.username = username
        self.pwd = pwd


def check(name):
    value = monitor_items[name]
    print(value)

if __name__ == '__main__':
    result = os.popen("/home/gateray/app/mongodb/bin/mongostat -n 1 1 --json").readline().strip()
    hostname = os.popen("hostname").readline().strip()
    monitor_items = json.loads(result)
    monitor_items = monitor_items[hostname]
    """
    {u'getmore': u'0',
     u'insert': u'*0',
     u'res': u'37.0M',
     u'time': u'17:46:34',
     u'netIn': u'79b',
     u'update': u'*0',
     u'host': u'gateray-pc',
     u'command': u'1|0',
     u'query': u'*0',
     u'netOut': u'15k',
     u'vsize': u'178.0M',
     u'conn': u'1',
     u'delete': u'*0'}
    res:物理内存占用(单位:g)
    vsize:虚拟内存占用(单位:g)
    netIn:通过网络流入字节数
    netOut:通过网络流出字节数
    """
    for k,v in monitor_items.items():
        if k in ("getmore","insert","update","delete","query") and "*" in v:
            monitor_items[k] = v[1:]
        elif k == "command":
            l = v.split("|")
            monitor_items[k] = int(l[0]) + int(l[1])
        elif k in ("res", "vsize"):
            if "m" in v.lower():
                monitor_items[k] = float(v[:-1])/1024
            elif "g" in v.lower():
                monitor_items[k] = float(v[:-1])
            else:
                monitor_items[k] = 0
        elif k in ("netIn","netOut"):
            if "b" in v.lower():
                monitor_items[k] = v[:-1]
            elif "k" in v.lower():
                monitor_items[k] = int(v[:-1])*1024
            elif "m" in v.lower():
                monitor_items[k] = int(v[:-1])*1024*1024
            elif "g" in v.lower():
                monitor_items[k] = int(v[:-1])*1024*1024*1024
    check(sys.argv[1])

