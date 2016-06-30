#!/usr/bin/env python
# coding: utf8

import MySQLdb

def channelmapping(cur):
    cur.execute('select id,name from bd_channel')
    rs = cur.fetchall()
    channel_map={}
    for r in rs:
        channel_map[r[0]]=r[1]
    return channel_map

try:
    conn = MySQLdb.connect(host='10.1.12.40',user='root',passwd='ASdf@#4atiow',port=3306,charset='utf8')
    cur = conn.cursor()
    conn.select_db('bingdu')
    channel_map = channelmapping(cur)
    count = cur.execute('select t2.uid,t1.sex,t2.channel_data from bd_user as t1, bd_my_channel as t2 where t2.uid=t1.user_id')
    print 'there are %d rows affect' %count
    stat_dict = {}
    rs = cur.fetchall()
    for r in rs:
        channels = r[2].split(',')
        for channel in channels:
            if channel != '' :
                stat_li = stat_dict.setdefault(channel_map[int(channel)],[0,0,0])
                stat_li[0] += 1
                if r[1] == 1:
                    stat_li[1] += 1
                else:
                    stat_li[2] += 1
    conn.commit()
    cur.close()
    conn.close()
except MySQLdb.Error,e:
    print "Mysql Error %d: %s" %(e.args[0],e.args[1])
except Exception,e:
    print e

print 'Channel Name\tUser Count\tMan Count\tGirl Count'
for k,v in stat_dict.items():
    print '{0:<17}\t{1:<10}\t{2:<9}\t{3:<10}'.format(k.encode('utf8'),*v)

