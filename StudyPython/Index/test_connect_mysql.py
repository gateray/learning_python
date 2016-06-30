#!/usr/bin/env python
# coding:utf8

import time
import MySQLdb
print '------------以列表的方式返回查询结果------------'
try:
    conn = MySQLdb.connect(host='127.0.0.1',user='root',passwd='root',
                           db='python_test',port=3306)
    cur = conn.cursor()
    key = 'j'
    print cur.execute('select * from user_info where name like %s', ('%s%%'%key,))
    print cur.fetchall()
    # print '----------------------------------------------------------'
    # cur.execute('insert into user_info(name) values (%s)',('nm',))
    # time.sleep(3)
    # print cur.lastrowid
    # print cur.lastrowid
    conn.commit()
    cur.close()
    conn.close()
except MySQLdb.Error,e:
    print 'Mysql Error Msg:', e
print '------------以字典的方式返回查询结果-------------'
# try:
#     conn = MySQLdb.connect(host='127.0.0.1',user='root',passwd='root',port=3306,db='python_test')
#     cur = conn.cursor(cursorclass = MySQLdb.cursors.DictCursor)
#     print cur.execute('select * from user_info')
#     print cur.fetchall()
#     cur.close()
#     conn.close()
# except MySQLdb.Error,e:
#     print 'Mysql Error Msg:', e
#
# def  fn(cur,*args,**kargs):
#     pass