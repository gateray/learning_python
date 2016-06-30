#!/usr/bin/env python
# coding:utf8
#

import re
import util,login_md
from datetime import date,datetime
session = {}
all = util.initdb()
trans = util.loadtrans()

def dologin():
    user = ss_getattr('user')
    if user:
        return user
    else:
        user = login_md.check_username()
        if not user: return False 
        if login_md.check_pwd(user):
            ss_setattr('user',user) 
            return user 
        else:
            return False

def ss_getattr(s):
    return session.get(s)   

def ss_setattr(s,obj):
    session.setdefault(s,obj)

def cleansession():
    session.clear()

def showatmview():
    print '~~ Welcome to atm ~~'
    d = {1:save_money_v,2:take_money_v,3:repay_money_v,4:transfer_money_v,5:list_account_v,6:list_transaction_v}
    while True:
        print '''
        (1) 存款
        (2) 取款
        (3) 还款
        (4) 转账
        (5) 查询
        (6) 交易查询
        (7) 退出'''    
        choice = util.input_choice(range(1,8))
        if choice == 7:
            util.serialize(all,'account.pkl')
            return dologout()
        if dologin() and not d[choice]():
            util.serialize(all,'account.pkl') 
            return dologout()
    
def save_money_v():
    while True:
        print '~~ 存款 ~~'
        ip = input_money()
        try:
            save_money(ip)
            if not util.iscontinue():break
        except Exception as e:
            raise e   
    return True

def take_money_v():
    while True:
        print '~~ 取款 ~~'
        ip = input_money()
        try:
            take_money(ip)
            if not util.iscontinue():break
        except Exception as e:
            raise e
    return True

def repay_money_v():
    while True:
        print '~~ 还款 ~~'
        ip = input_money()
        try:
            repay_money(ip)
            if not util.iscontinue():break
        except Exception as e:
            raise e
    return True

def transfer_money_v():
    while True:
        print '~~ 转账 ~~'
        ip = input_money()
        ip_ac = input_tfaccount()
        try:
            transfer_money(ip,ip_ac)
            if not util.iscontinue():break
        except Exception as e:
            raise e
    return True

def list_account_v():
    while True:
        print '~~ 查询 ~~'
        try:
            list_account()
            if not util.iscontinue():break
        except Exception as e:
            raise e
    return True

def list_transaction_v():
    while True:
        print '~~ 交易查询 ~~'
        dt_l = input_date()
        try:
            list_transaction(dt_l)
            if not util.iscontinue():break
        except Exception as e:
            raise e
    return True

def input_money():
    while True:
        try:
            money = float(raw_input('请输入金额: ').strip())
            return money
        except ValueError:
            continue

def input_tfaccount():
    while True:
        account = raw_input('请输入转账目标账号: ').strip()
        if re.match(r'^\d{4,}$',account):
            return account
        else:
            print '账号格式有误，请重新输入！'
        
            
def input_date():
    while True:
        start = raw_input('请输入起始日期: ').strip()
        end = raw_input('请输入结束日期: ').strip()
        try:
            start_dt = datetime.strptime(start,'%Y-%m-%d')
            end_dt = datetime.strptime(end,'%Y-%m-%d')
            if start_dt > end_dt:
                print '起始日期不能大于结束日期！'
                continue
            else:
                return start_dt,end_dt
        except ValueError:
            continue 


def aop(func):
    def logtrans(user,retval):
        if not retval: return retval
        ac_name = user.keys()[0]
        jytime = str(datetime.now())
        jytype = retval[1]
        jymoney = retval[2]
        zrmoney = retval[3]
        zcmoney = retval[4]
        trans.setdefault(ac_name,[]).append([jytime,jytype,jymoney,zrmoney,zcmoney])
        util.transaction(trans)     
    def _deco(*args,**kargs):
        user = ss_getattr('user') 
        if not user:
            user = dologin()
            if not user: return False
        if 'list_' in func.__name__:
            return func(*args,**kargs)
        print '操作前金额：'
        list_account()
        retval = func(*args,**kargs)
        print '操作后金额：'
        list_account()
        logtrans(user,retval)
        return retval
    return _deco


@aop
def save_money(money):
    user = ss_getattr('user') 
    key = user.keys()[0]
    user[key][2] += money
    user[key][3] += money
    return (None,'存款', money, money, 0)

@aop
def take_money(money):
    user = ss_getattr('user')
    key = user.keys()[0]
    if user[key][5] == 0:
        print '当前信用卡处于欠款状态不可用，请及时还款！'
        return False
    if user[key][3] < (money*1.05):
        print '金额不足，操作失败！'
        return False
    if user[key][2] > (money*1.05):
        user[key][2] -= (money*1.05)
    else:
        user[key][2] = 0
    user[key][3] -= (money*1.05)
    return (None,'取款', money*1.05, 0, money*1.05)

@aop
def consume(money,btype):
    print '正在调用支付接口。。。'
    user = ss_getattr('user')
    key = user.keys()[0]
    if user[key][5] == 0:
        print '当前信用卡处于欠款状态不可用，请及时还款！'
        return False
    if user[key][3] < money:
        print '金额不足，操作失败！'
        return False
    if user[key][2] > money:
        user[key][2] -= money
    else:
        user[key][2] = 0
    user[key][3] -= money
    util.serialize(all,'account.pkl')
    return (None, btype, money, 0, money)    

@aop
def repay_money(money):
    user = ss_getattr('user')
    key = user.keys()[0]
    qiankuan = user[key][4]
    if money < qiankuan:
        user[key][4] -= money
        print '欠款尚未还清！'
    else:
        user[key][4] = 0
        user[key][2] += (money-qiankuan) 
        user[key][5] = 1
    return (None,'还款', money, money, 0) 

@aop
def transfer_money(money,tfaccount):
    user = ss_getattr('user')
    key = user.keys()[0]
    if user[key][5] == 0:
        print '当前信用卡处于欠款状态不可用，请及时还款！'
        return False
    if user[key][3] < (money*1.05):
        print '金额不足，操作失败！'
        return False
    if user[key][2] > (money*1.05):
        user[key][2] -= (money*1.05)
    else:
        user[key][2] = 0
    user[key][3] -= (money*1.05)
    if tfaccount in all:
        all[tfaccount][2] += money
        all[tfaccount][3] += money       
    return (None,'转账', money*1.05, 0, money*1.05) 

@aop
def list_account():
    user = ss_getattr('user')
    title = ['账号','密码','固定额度','溢缴款','可用额度','累计欠款','信用卡状态','账户可操作状态']
    o_l = util.dict2list(user)
    util.showtable(title,o_l)

@aop
def list_transaction(dt_l):
    user = ss_getattr('user')    
    start_dt,end_dt = dt_l
    start = end = None
    ac_name = user.keys()[0]
    o_l = trans.get(ac_name)
    if o_l is None:
        print '暂无交易记录！'
        return
    for i,l in enumerate(o_l):
        if start_dt <= datetime.strptime(l[0],'%Y-%m-%d %H:%M:%S.%f') and start is None:
            start = i
        elif start is None:
            continue
        elif end_dt < datetime.strptime(l[0],'%Y-%m-%d %H:%M:%S.%f') and end is None:
            end = i
            break
        elif i == len(o_l) - 1:
            end = len(o_l)
    if start is None:
        print '暂无交易记录！'
        return
    ml = o_l[start:end]
    sl = []
    for l in ml:
        sl.append([ac_name]+l)              
    title = ['账号', '交易时间','交易类型','交易金额','支入金额','支出金额']
    util.showtable(title,sl)

def bill():
    now = date.today()
    if now.day == 30:
        for k,v in all:
            qiankuan = v[1] - v[3]
            if qiankuan > 0:
                v[4] += qiankuan
            v[3] += v[1]
    elif now.day == 10:
        for k,v in all:
            repay_money(v[2])
    elif now.day > 10:
        for k,v in all:     
            v[4] += (v[4]*0.05)
            if v[4] > 0:
                v[5] = 0
    
def dologout():
    if len(session) != 0: cleansession()
    return False
