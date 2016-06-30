#!/usr/bin/env python
#coding: utf8

import xlrd
import MySQLdb
import sys

excel = xlrd.open_workbook(sys.argv[1])
sheet = excel.sheet_by_name('Sheet2')
rows_count = sheet.nrows
print rows_count
db = MySQLdb.connect('10.1.12.42','root','mysqlnhzw_2988','bingdu')

cur = db.cursor()
i = 0

while i < rows_count:
    uid = int(sheet.cell(i,0).value)
    discard_cash = sheet.cell(i,2).value
    sql1 = 'select uid,cash_income from bd_point_user_info where uid=%d' %uid
    sql2 = 'update bd_point_user_info set cash_income = cash_income - %s where uid = %d'%(discard_cash,uid)
    cur.execute(sql1)
    rs = cur.fetchone()
    print 'before discard: uid:%d        cash_income:%s' %rs
    try:
        cur.execute(sql2)
        db.commit()
    except:
        db.rollback()
    i += 1
    print "row_id: %d     uid: %d       discard_cash: %d"%(i,uid,discard_cash)
    cur.execute(sql1)
    rs = cur.fetchone()
    print 'after discard: uid:%d        cash_income:%s' %rs

cur.close()
db.close()