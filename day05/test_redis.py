#!/usr/bin/env python
# coding: utf8

import MySQLdb
import redis

try:
    db = MySQLdb.connect('10.1.12.42', 'root', 'mysqlnhzw_2988', 'bingdu',charset='utf8')
    r = redis.Redis(host='10.1.12.21',port=6379,db=4)
    cur = db.cursor()
    print r.rpop("queue:news:stat_bak5")
    #根据用户nickname查找uid
    #getuid = "select t.uid from bd_point_withdraw_record t where t.pay_account REGEXP '^[a-z]{3,4}[0-9]{5}@126.com$'"
    # reg = u'^并读(管理员|客服)'.encode('utf8')
    # getuid = "select user_id from bd_user where nick_name rlike '%s'" %reg

    # getuid = "select DISTINCT t.uid from bd_point_withdraw_record t where t.pay_account REGEXP '^[a-z]{4}[0-9]{4,6}@163.com$' order by t.uid"
    # count = cur.execute(getuid)
    # print "total records: %d" %count
    # rs = cur.fetchall()
    # #要排除的uid
    # uids = [427591,
    #         444417,
    #         444457,
    #         449235
    # ]

    # maps = {
    #     'blockUser:%d:0' : '{"blockEndTime":2117030399032,"blockFromTime":1435649612032,"blockTimeDuration":"FF","blockType":0,"createTime":1435649612032,"id":%d,"uid":%d}',
    #     'markedUser:%d' : '{"bindAccountCount":0,"uid":%d}'
    # }
    #select t.uid from bd_point_withdraw_record t where t.pay_account REGEXP '^[a-z]{3,4}[0-9]{5}@126.com$'

    # for row in rs:
    #     uid = int(row[0])
    #     if uid in uids: continue
    #     print 'uid: %d' %uid
    #     #通过uid插入永久禁言
    #     insertuid = "INSERT INTO `bd_user_block` (`uid`, `block_type`, `block_time_duration`, `block_from_time`, `block_end_time`, `create_time`) VALUES ('%d', '0', 'FF', CURTIME(), '2037-02-01 00:00:00', CURTIME())" %uid
    #     cur.execute(insertuid)
    #     #获取uid对应的id
    #     getid = "SELECT id FROM bd_user_block WHERE uid='%d' AND block_type=0 AND block_time_duration='FF'" %uid
    #     cur.execute(getid)
    #     id = int(cur.fetchone()[0])
    #     db.commit()
        #插入uid和id的记录到redis
    #     key1 = 'blockUser:%d:0'%int(uid)
    #     value1 =  '{"blockEndTime":2117030399032,"blockFromTime":1435649612032,"blockTimeDuration":"FF","blockType":0,"createTime":1435649612032,"id":%d,"uid":%d}'%(id,uid)
    #     print key1," | ",value1
    #     r.setnx(key1,value1)
    #     key2 = 'markedUser:%d'%uid
    #     value2 = '{"bindAccountCount":0,"uid":%d}'%uid
    #     print key2," | ",value2
    #     r.setnx(key2,value2)
    # print "total records: %d" %count
except MySQLdb.MySQLError as e:
    print e
    db.rollback()
except Exception as e:
    print e
