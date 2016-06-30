#!/usr/bin/env python
# coding:utf8

import util
import dao.mysqlhelper as dm

def wrapper(fn):
    def _deco(*args,**kargs):
        conn_args = util.loadconfig()['mysqlconfig']
        conn = None
        cur = None
        try:
            conn = MySQLdb.connect(host=conn_args['MYSQL_HOST'],port=conn_args['MYSQL_PORT'],user=conn_args['MYSQL_USER'],
                                    passwd=conn_args['MYSQL_PASSWD'],db=conn_args['MYSQL_DB'],charset='utf8')
            cur = conn.cursor(cursorclass=MySQLdb.cursors.DictCursor)
            kargs['cur'] = cur
            reval = fn(*args,**kargs)
            conn.commit()
            return reval
        except MySQLdb.Error, e:
            print e
            raise e
        except Exception, e:
            print e
            raise e
        finally:
            if cur:cur.close()
            if conn:conn.close()
    return _deco 

@wrapper
def regist(user,cur=None):
    sql = util.loadconfig()['sql']['queryuserbyname']
    u = dm.queryuserbyname(cur,sql,user.__dict__)
    if u:
        return {'err':'用户已存在'}    
    else:
        sql = util.loadconfig()['sql']['insertuser']
        return dm.insertuser(cur,sql,user.__dict__)
    
@wrapper
def login(user,cur=None):
    sql = util.loadconfig()['sql']['queryuserbyname']
    u = dm.queryuserbyname(cur,sql,user.__dict__)
    if u.pwd == user.pwd:
        return u
    else:
        return {'err':'登陆失败'}

@wrapper
def showchatlog(cpgid,user,cur=None):
    sql = util.loadconfig()['sql']['querychatlog']
    kargs = {'s_uid':user.id,'r_uid':user.id}
    return dm.querychatlog(cur,cpgid,sql,kargs)

def showchatlogbydt(cpgid,user,b_tm,e_tm,cur=None):
    sql = util.loadconfig()['sql']['querychatlogbydt']
    kargs = {'s_uid':user.id,'r_uid':user.od,'b_tm':b_tm,'e_tm':e_tm}
    return dm.querychatlogbydt(cur,cpgid,sql,kargs)

def getanswer(qa,cur=None):
    sql = util.loadconfig()['sql']['queryanswer']
    kargs = {'question':qa.question}
    return dm.queryanswer(cur,sql,kargs)

def createqa(qa,cur=None):
    sql = util.loadconfig()['sql']['insertqa']
    return insertqa(cur,sql,qa.__dict__)
