#!/usr/bin/env python
# coding:utf8
#
basedir = '/var/log/'
log = [basedir + f % n for n in range(20) for f in ['syslog.log.%d','message.log.%d','secure.log.%d']]
a=1
def func():
    #global log
    log = []
    for i in log:
        yield i

if __name__ == '__main__':
    for i in func():
        print i
    print '-------------------------'
    print log
