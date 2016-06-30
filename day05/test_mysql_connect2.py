#!/usr/bin/env python
# coding: utf8

import MySQLdb

try:
    conn = MySQLdb.connect(host='localhost',user='root',passwd='mysql',port=3306)
    cur = conn.cursor()
    print '------> call excute() to create a database python'
    cur.execute('create database if not exists python')
    print '------> call select_db() to use database python'
    conn.select_db('python')
    print '------> call execute() to create a table test'
    cur.execute('create table test(id int,info varchar(20))')
    print '------> call execute() to insert 1 row'
    value = [1,'hi rollen']
    cur.execute('insert into test values(%s,%s)',value)
    
    values = []
    for i in range(20):
        values.append((i,'hi rollen'+str(i)))
    print '------> call executemany() to insert multi rows'
    cur.executemany('insert into test values(%s,%s)',values)
    print '------> call execute() to update one rows'
    cur.execute('update test set info="I am rollen" where id=3')
    print '------> call commit()'
    conn.commit()
    cur.close()
    conn.close()
except MySQLdb.Error,e:
    print "Mysql Error %d: %s"%(e.args[0],e.args[1])
