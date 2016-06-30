#!/usr/bin/env python
# coding:utf8
#

import pickle
import hashlib
import os.path
from prettytable import PrettyTable 

def serialize(obj,pklfile):
    with open(pklfile,'w') as f:
        pickle.dump(obj,f)

def deserialize(pklfile):
    with open(pklfile,'r') as f:
        return pickle.load(f)

def md5(pwd):
    md5 = hashlib.md5()
    md5.update(pwd)
    return md5.hexdigest()

def initdb():
    tab_account = 'account.pkl'
    if os.path.isfile(tab_account):
        return deserialize(tab_account)
    else:
        #账号:[密码md5，固定额度，溢缴款，可用额度，累计欠款，信用卡状态，账户可操作状态]
        d = dict(zip(('0000','0001','0002','0003'),[
                    [md5('0000'),15000,0,15000,0,1,1],
                    [md5('0001'),15000,0,15000,0,1,1],
                    [md5('0002'),15000,0,15000,0,1,1],
                    [md5('0003'),15000,0,15000,0,1,1]])) 
        serialize(d,tab_account)
        return d

def transaction(trans):
    #obj={账号:[[交易时间，交易类型，交易金额，支入金额，支出金额],...]}
    tab_transaction = 'transaction.pkl'
    serialize(trans,tab_transaction)

def loadtrans():
    tab_transaction = 'transaction.pkl' 
    if os.path.isfile(tab_transaction):
        return deserialize(tab_transaction)
    else:
        return {}

def iscontinue():
    return raw_input('是否继续(Y/N)? ').strip() in 'y'

def dict2list(obj):
    l = []
    for k,v in obj.items():
        tmp_l = []
        tmp_l.append(k)
        l.append(tmp_l + v)
    return l

def showtable(title,o_l):
    table = PrettyTable(title)
    table.align[title[0]] = 'l'
    table.padding_width = 1
    for i in o_l:
        table.add_row(i)
    print table

def input_choice(l):
    while True:
        choice = raw_input('Your choice is: ').strip()
        if choice.isdigit() and int(choice) in l:
            return int(choice)
        else:
            print '输入有误，请重新输入！'
