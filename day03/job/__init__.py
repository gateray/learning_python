#!/usr/bin/env python
# coding:utf8
#
import atm
import login_md
import util
import shopping

if __name__ == '__main__':
    while True:
        print '''
        (1) ATM
        (2) 购物
        (3) 退出'''
        choice = util.input_choice(range(1,4))
        tonext = {1:atm.showatmview,2:shopping.showshoppingview,3:exit}
        try:
            tonext[choice]()
        except KeyboardInterrupt:
            util.serialize(atm.all,'account.pkl')
            print '\n'
            exit()
