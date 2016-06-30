#!/usr/bin/env python
# coding: utf8

import xlrd
import MySQLdb
import sys
import time
import redis

excel = xlrd.open_workbook(sys.argv[1])
sheet = excel.sheet_by_name('Sheet1')
sheets = excel.sheets()
print sheets
rows_count = sheet.nrows
print rows_count

db = MySQLdb.connect('10.1.12.42', 'root', 'mysqlnhzw_2988', 'bingdu')
r = redis.Redis(host='10.1.12.21',port=6379,db=0)

cur = db.cursor()
i = 0

while i < rows_count:
    try:
        uid = int(sheet.cell(i, 0).value)
        #discard_cash = sheet.cell(i,2).value
        add_point = sheet.cell(i, 1).value

        sql1 = 'select * from bd_point_user_daily_record t where t.uid = %d and t.statistics_date = CURDATE()' % uid
        count = cur.execute(sql1)
        if count != 0:
            sql2 = 'update bd_point_user_daily_record t set t.today_point = t.today_point + %s where t.uid = %d and t.statistics_date = CURDATE()' % (add_point, uid)
            cur.execute(sql2)
        else:
            sql3 = 'insert into bd_point_user_daily_record (uid,today_point,today_income,statistics_date,archived,update_time) values(%d,%s,0,CURDATE(),0,CURDATE())' % (uid, add_point)
            cur.execute(sql3)
        sql4 = 'insert into bd_point_upper_bound(uid, op_num,op_type, op_point, op_date) values(%d,1,13,%s,CURDATE())' % (uid, add_point)
        cur.execute(sql4)
        db.commit()
        key = 'point:bound:23:13:%d'%uid
        value = '{\"id\":33929970,\"opDate\":1435021073606,\"opNum\":1,\"opPoint\":%s,\"opType\":13,\"uid\":%d}'%(add_point,uid)
        r.set(key,value,30000)

        print uid
        #time.sleep(0.1)
        i += 1
    except MySQLdb.MySQLError as e:
        print e
        db.rollback()
    except Exception as e:
        print e
