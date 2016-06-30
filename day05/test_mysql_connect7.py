#!/usr/bin/env python
# coding: utf8
'''
用户标红+禁言
将uid粘贴到同级目录的uid.txt文件中,执行脚本即可
'''

import MySQLdb
import redis

try:
    db = MySQLdb.connect('10.1.12.42', 'root', 'mysqlnhzw_2988', 'bingdu',charset='utf8')
    r = redis.Redis(host='10.1.12.21',port=6379,db=0)
    cur = db.cursor()


    with open('uid.txt') as f:
        for row in f:
            uid = int(row)
            #通过uid插入永久禁言
            insertuid = "INSERT INTO `bd_user_block` (`uid`, `block_type`, `block_time_duration`, `block_from_time`, `block_end_time`, `create_time`) VALUES ('%d', '0', 'FF', CURTIME(), '2037-02-01 00:00:00', CURTIME())" %uid
            cur.execute(insertuid)
            #获取uid对应的id
            getid = "SELECT id FROM bd_user_block WHERE uid='%d' AND block_type=0 AND block_time_duration='FF'" %uid
            cur.execute(getid)
            id = int(cur.fetchone()[0])
            db.commit()
            #插入uid和id的记录到redis
            key1 = 'blockUser:%d:0'%int(uid)
            value1 =  '{"blockEndTime":2117030399032,"blockFromTime":1435649612032,"blockTimeDuration":"FF","blockType":0,"createTime":1435649612032,"id":%d,"uid":%d}'%(id,uid)
            print key1," | ",value1
            if not r.setnx(key1,value1) : r.set(key1,value1)
            key2 = 'markedUser:%d'%uid
            value2 = '{"bindAccountCount":0,"uid":%d}'%uid
            print key2," | ",value2
            if not r.setnx(key2,value2) : r.set(key2,value2)
except MySQLdb.MySQLError as e:
    print e
    db.rollback()
except Exception as e:
    print e
