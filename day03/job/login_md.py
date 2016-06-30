#!/usr/bin/env python
# coding:utf8
#

import re
import util
import atm

def check_username():
    for i in range(3):
        name = raw_input('输入账号: ').strip()
        if re.match(r'\d{4}', name) and name in atm.all:
            if atm.all[name][6] == 0:
                print '账号已被锁定！'
                return False
            return {name:atm.all[name]}
        print '账号不存在！'
    return False

def check_pwd(user):
    ac_name = user.keys()[0]
    for i in range(3):
        pwd = raw_input('输入密码: ')
        if len(pwd) == 4 and util.md5(pwd) == user[ac_name][0]: 
            return True
    dolock(user)
    print '账号：%s已被锁定！' %(ac_name)
    return False

def dolock(user):
    ac_name = user.keys()[0]
    user[ac_name][6] = 0
