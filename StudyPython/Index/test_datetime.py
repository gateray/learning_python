#!/usr/bin/env python
# coding:utf8
from datetime import date, datetime
import time

now= date.today()
print now
tomorrow = now.replace(day=25)
print tomorrow
print now.weekday()
print tomorrow.weekday()
print type(date.today().day),date.today().day
date_now = datetime.now()  # 当前日期
m = date_now.strftime('%m')
start1 = date_now.strftime('%Y-%m-1')
start2 = datetime.strptime(start1,'%Y-%m-%d')
print m 
print start1
print start2
print type(start1),type(start2)   

start = datetime(2014,12,1)
print start
start = datetime.now()
#time.sleep(2)
end = datetime.now()
start_str = start.strftime('%Y-%m-%d %H:%M:%S')
end_str = end.strftime('%Y-%m-%d %H:%M:%S')
start = datetime.strptime(start_str,'%Y-%m-%d %H:%M:%S')
end = datetime.strptime(end_str,'%Y-%m-%d %H:%M:%S')
print start > end
print start < end
print datetime.now()


print '-----------------------------------'
print datetime.strptime('2015-01-07 16:37:29.884820','%Y-%m-%d %H:%M:%S.%f')
print time.ctime()
print '-------（时间戳与时间字符串互相转化）----------'
a = '2015-1-10 20:20:20'
target = time.strptime(a, '%Y-%m-%d %H:%M:%S') #转换结果为time.struct_time对象
print target
#将time.struct_time对象转换为时间戳
print time.mktime(target)
print datetime.fromtimestamp(1420892420.111)
print time.strftime('%Y-%m-%d %H:%M:%S')