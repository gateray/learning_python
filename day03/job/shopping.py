#!/usr/bin/env python
# coding:utf8

import re
import util
import atm

cart = {}

def add2cart(it):
    return cart.setdefault(it[0],it[1]) 

def paymoney():
    total = gettotal()
    print '-------total: %d-------' %total
    if total == 0: return
    if atm.consume(total,'makelove'):
        print '支付成功！'
        clearcart() 
    else:
        print '支付失败！'

def showcart():
    if not cart:
        print '当前购物车为空！'
        return
    title = ['商品', '单价', '数量']   
    util.showtable(title,cart.values())
    print '总价：%d' %(reduce(lambda x,y:x+y, [v[1]*v[2] for v in cart.values()]))

def clearcart():
    cart.clear()

def gettotal():
    if not cart: return 0
    return reduce(lambda x,y:x+y, [v[1]*v[2] for v in cart.values()])

def input_amount(l):
    while True:
        amount = raw_input('请输入你要购买的%s数量: ' %l[0])
        if amount.isdigit() and int(amount) > 0:
            return int(amount)

def showshoppingview():
    goods = [['apple',1000, 0],['banana',2000, 0],['pear',3000, 0],['mango',4000, 0],['melon',5000, 0]]
    while True: 
        print '商品编号  商品名称      单价'
        print '-'*30
        for num,item in enumerate(goods,1):
            print '%-10d%8s%10s' % (num,item[0],item[1])
        choice = util.input_choice(range(1,len(goods)+1))
        amount = input_amount(goods[choice-1])
        goods[choice-1][2] += amount
        add2cart((choice,goods[choice-1]))
        payview()
        if not util.iscontinue():
            atm.dologout()
            break

def payview():
    while True:
        print '''
        <1>查看购物车<2>返回继续购物<3>清空购物车<4>结算'''
        choice = util.input_choice(range(1,5))
        callto={1:showcart,3:clearcart,4:paymoney}
        if choice == 2:break
        callto[choice]() 
