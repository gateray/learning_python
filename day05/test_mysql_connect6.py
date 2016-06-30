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

def reducechannelcount(exclude_li,stat_dict,channel_map,sex):
    index = 1
    if sex == 0:
        index = 2
    for chan in exclude_li:
        stat_li = stat_dict.setdefault(channel_map[chan],[(init_man_count+init_girl_count),init_man_count,init_girl_count])
        stat_li[0] -= 1
        stat_li[index] -= 1

try:
    conn = MySQLdb.connect(host='10.1.12.40',user='root',passwd='ASdf@#4atiow',port=3306,charset='utf8')
    cur = conn.cursor()
    conn.select_db('bingdu')
    channel_map = channelmapping(cur)

    cur.execute('select count(*) from bd_user group by sex')
    rs = cur.fetchmany(2)
    init_girl_count = rs[0][0]
    init_man_count = rs[1][0]

    count = cur.execute('select t2.uid,t1.sex,t2.channel_data from bd_user as t1, bd_my_channel as t2 where t2.uid=t1.user_id')
    stat_dict = {}
    def_channels = [1,2,3,4,46,41,37,62]
    rs = cur.fetchall()
    for r in rs:
        if r[1] not in (0,1): continue
        exclude_li = list(def_channels)
        channels = r[2].split(',')
        for channel in channels:
            if channel != '' :
                chan = int(channel)
                if chan not in def_channels:
                    stat_li = stat_dict.setdefault(channel_map[chan],[0,0,0])
                    stat_li[0] += 1
                    if r[1] == 1:
                        stat_li[1] += 1
                    else:
                        stat_li[2] += 1
                else:
                    stat_dict.setdefault(channel_map[chan],[(init_man_count+init_girl_count),init_man_count,init_girl_count])
                    exclude_li.remove(chan)
                    continue
        reducechannelcount(exclude_li,stat_dict,channel_map,r[1])
    conn.commit()
    cur.close()
    conn.close()
except MySQLdb.Error,e:
    print "Mysql Error %d: %s" %(e.args[0],e.args[1])
except Exception,e:
    print e.message

print 'Channel Name\tUser Counts\tMen Counts\tWomen Counts'
for k,v in stat_dict.items():
    print '{0:<17}\t{1:<11}\t{2:<10}\t{3:<12}'.format(k.encode('utf8'),*v)

