#!/usr/bin/env python
# coding: utf8

import MySQLdb

try:
    conn = MySQLdb.connect(host='localhost',user='root',passwd='mysql',port=3306)
    cur = conn.cursor()
    conn.select_db('python')
    print '------> call execute() to select all rows return a rowcount'
    count = cur.execute('select * from test')
    print 'there has %d rows record' %count

    print '------> call fetchone() to get one row content'
    result = cur.fetchone()
    print result
    print 'ID: %d info: %s' % result
    print '------> call fetchmany() to get 5 rows'
    results=cur.fetchmany(5)
    for r in results:
        print r
    print '=='*10
    print '------> call scroll() set the cursor to begin of table'
    cur.scroll(0,mode='absolute')
    print '------> call fetchall() to get all rows'
    results = cur.fetchall()
    for r in results:
        print r[1]
    print '------> call commit()'
    conn.commit()
    cur.close()
    conn.close()
except MySQLdb.Error,e:
    print "Mysql Error %d: %s" %(e.args[0],e.args[1])
