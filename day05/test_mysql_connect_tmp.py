#!/usr/bin/env python
# coding: utf8
# description: 标红+余额清零

import MySQLdb
import redis

writelist = []
r = None
db = None

def getredisconnection():
    global r
    if not r:
        try:
            r = redis.Redis(host='10.1.12.21',port=6379,db=0)
        except Exception,e:
            print e
            exit()
    return r

def getmysqlconnection():
    global db
    if not db:
        try:
            db = MySQLdb.connect('10.1.12.42', 'root', 'mysqlnhzw_2988', 'bingdu',charset='utf8')
        except Exception,e:
            print e
            exit()
    return db

def biaohong(uid):
    r = getredisconnection()
    try:
        key = 'markedUser:%d'%uid
        value = '{"bindAccountCount":0,"uid":%d}'%uid
        r.setnx(key,value)
    except redis.RedisError,e:
        print e
    except Exception,e:
        print e

def cancelbiaohong(uid):
    r = getredisconnection()
    try:
        key = 'markedUser:%d'%uid
        #value = '{"bindAccountCount":0,"uid":%d}'%uid
        r.delete(key)
    except redis.RedisError,e:
        print e
    except Exception,e:
        print e

def moneytozero(uid):
    try:
        db = getmysqlconnection()
        r = getredisconnection()
        cur = db.cursor()
        sql = 'update bd_point_user_info set cash_income = 0 where uid = %d' %(uid)
        cur.execute(sql)
        db.commit()
        key = 'point:user:%d'%uid
        if r.exists(key):r.delete(key)
    except MySQLdb.MySQLError,e:
        print e
        db.rollback()
    except Exception,e:
        print e

def changemoneytospecialvalue(uid):
    try:
        # db = getmysqlconnection()
        r = getredisconnection()
        # cur = db.cursor()
        # fetch_cash = 'select withdraw_money from bd_point_withdraw_record where uid=%d'%uid
        # cur.execute(fetch_cash)
        # rs = cur.fetchall()
        # for row in rs:
        #     change_money = 'update bd_point_user_info set cash_income = cash_income + %s where uid = %d' %(row[0],uid)
        #     cur.execute(change_money)
        # db.commit()
        key = 'point:user:%d'%uid
        if r.exists(key):r.delete(key)
    # except MySQLdb.MySQLError, e:
    #     print e
    #     db.rollback()
    except Exception,e:
        print e

if __name__ == '__main__':
    with open('uid.txt') as f:
        for struid in f:
            uid = int(struid)
            changemoneytospecialvalue(uid)
            print uid
