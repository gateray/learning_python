#!/usr/bin/env python
# coding:utf8

import util,factory
import MySQLdb

def queryone(cur,sql,kargs,rtclass_name):
    cur.execute(sql,kargs)
    d = cur.fetchone()
    return factory.dict2obj(d,rtclass_name)

def insertone(cur,sql,kargs):
    return cur.execute(sql,kargs)

def querychatlogcount(cur,sql):
    cur.execute(sql)
    return cur.fetchone().values()[0]

def querychatlogwithpage(cur,cpgid,sql,kargs):
    pgsize = 20
    allrecord = querychatlogcount(cur,util.loadconfig()['sql']['querychatlogcount'])
    offset = (cpgid-1)*pgsize
    pgcount = (allrecord-1)/pgsize + 1
    cur.execute(sql,kargs)
    cur.scroll(offset,mode='absolute')
    ds = cur.fetchmany(pgsize)
    content = []
    for d in ds:
        content.append(factory.dict2obj(d,util.loadconfig()['messageclass']))
    frsize = 10
    frloffset = 5
    lpgid = (cpgid-frloffset) if cpgid > frloffset else 1
    rpgid = pgcount if (lpgid+frsize-1) >= pgcount else (lpgid+frsize-1)
    pgdict = {'pgsize':pgsize,'allrecord':allrecord,'pgcount':pgcount,'cpgid':cpgid,'content':content,'frsize':frsize,
                'frloffset':frloffset,'lpgid':lpgid,'rpgid':rpgid}
    return factory.dict2obj(pgdict,util.loadconfig()['pgclass']) 
    
def queryuserbyname(cur,sql,kargs):
    return queryone(cur,sql,kargs,util.loadconfig()['userclass']) 

def queryuserbyid(cur,sql,kargs):
    return queryone(cur,sql,kargs,util.loadconfig()['userclass'])

def insertuser(cur,sql,kargs):
    return insertone(cur,sql,kargs)

def querychatlog(cur,cpgid,sql,kargs):
    return querychatlogwithpage(cur,cpgid,sql,kargs)
     
def querychatlogbydt(cur,cpgid,sql,kargs):
    return querychatlogwithpage(cur,cpgid,sql,kargs)

def insertchatlog(cur,sql,kargs):
    return insertone(cur,sql,kargs)

def queryanswer(cur,sql,kargs):
    queryone(cur,sql,kargs,util.loadconfig()['QA'])

def insertqa(cur,sql,kargs):
    return insertone(cur,sql,kargs)
