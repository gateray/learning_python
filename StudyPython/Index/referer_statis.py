#!/usr/bin/env python
# coding: utf8

import re

logfile = '/home/gateray/桌面/cdn-logs/2015-10-10-0000-2330_image.bingodu.com.cn.log'
pattern = r'((\d+\.){3}\d+)\s+(\w+|-)\s+(\w+|-)\s+(\[.*\])\s+"(.*)"\s+(\d+)\s+(\d+)\s+"(.*)"\s+"(.*)"'
hitword = r'(?:http|https)://(.*?(?=/)|[^/]*$)'
dic = {}
with open(logfile,'r') as f:
    for line in f:
        m = re.match(pattern,line)
        referer = m.group(9)
        if len(referer)!=0 and 'bingodu.com' not in referer:
            try:
                host = re.match(hitword,referer).group(1)
                dic[host] = dic.setdefault(host,0)+1
            except AttributeError:
                dic[referer] = dic.setdefault(referer,0)+1

print 'Total: %s'%len(dic)

li = sorted(dic.iteritems(),key=lambda elm:elm[1],reverse=True)
for k,v in li:
    print "host: %s, total: %d"%(k,v)
print 'Total: %s'%len(dic)





