#!/usr/bin/env python
# coding:utf8

import util
import dao.mysqlhelper as dm
from factory import BeanFactory

print '-------------------test BeanFactory,getInstance()-----------------'
user = BeanFactory.getInstance(util.loadconfig()['userclass'])
print user.convert()

print '-----------------test queryuserbyname(cur,sql,kargs):-----------------'
sql = util.loadconfig()['sql']['queryuserbyname']
print dm.queryuserbyname(None,sql,{'name':'user1'})

print '-----------------test queryuserbyid(cur,sql,kargs)-------------------'
sql = util.loadconfig()['sql']['queryuserbyid']
print dm.queryuserbyid(None,sql,{'id':1})

print '-----------------test insertuser(cur,sql,kargs)------------'
sql = util.loadconfig()['sql']['insertuser']
print dm.insertuser(None,sql,{'name':'user2','pwd':'670b14728ad9902aecba32e22fa4f6bd'})

print '-----------------test '
