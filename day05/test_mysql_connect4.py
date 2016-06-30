#!/usr/bin/env python
# coding: utf8

import MySQLdb

try:
    conn = MySQLdb.connect(host='localhost',user='root',passwd='mysql',port=3306)
    cur = conn.cursor()
    conn.select_db('07day05')
    print '------> call execute() to select all rows return a rowcount'
    count = cur.execute('select * from t_message')
    print 'there has %d rows record' %count

    print '------> call fetchone() to get one row content'
    result = cur.fetchone()
    print result[0], result[1],result[2], type(result[3]),result[4]
    conn.commit()
    cur.close()
    conn.close()
except MySQLdb.Error,e:
    print "Mysql Error %d: %s" %(e.args[0],e.args[1])
