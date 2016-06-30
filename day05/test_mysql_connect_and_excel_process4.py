#!/usr/bin/env python
# coding: utf8
# description: "批量修改用户订单状态"
import xlrd
import MySQLdb
import sys

excel = xlrd.open_workbook(sys.argv[1])
sheet = excel.sheet_by_name('Sheet1')
rows_count = sheet.nrows
print rows_count
db = MySQLdb.connect('10.1.12.42','root','mysqlnhzw_2988','bingdu')

cur = db.cursor()

for i in range(rows_count):
    oid = int(sheet.cell(i,0).value)
    sql1 = 'SELECT id,status FROM `bd_goods_orders` WHERE id = %d' %oid
    sql2 = 'UPDATE `bd_goods_orders` SET status = 1 WHERE id = %d' %oid
    cur.execute(sql1)
    rs = cur.fetchone()
    print 'before: id:%d       status:%s' %rs
    try:
        cur.execute(sql2)
        db.commit()
    except:
        db.rollback()

    print "row_id: %d     id: %d" % (i,oid)
cur.close()
db.close()