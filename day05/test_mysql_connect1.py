#!/usr/bin/env python
# coding: utf8

import MySQLdb
try:
    conn = MySQLdb.connect(host='localhost',user='root',passwd='mysql',port=3306,db='mysql')
    cur = conn.cursor()
    cur.execute('select User,Password,Host from user')
    print 'call ----------------> fetchall()'
    print cur.fetchall()
    print 'call ----------------> scroll(row_cursor,mode="absolute")'
    cur.scroll(0,mode='absolute') #same as "cur.scroll(0,'absolute')"
    print 'call ----------------> fetchmany(size)'
    print cur.fetchmany(2)
    print 'call ----------------> fetchmay(size) again'
    print cur.fetchmany(2)
    print 'call ----------------> fetchone()'
    print cur.fetchone()
    cur.close()
    conn.close()
except MySQLdb.Error,e:
    print 'Mysql Error Msg:', e
