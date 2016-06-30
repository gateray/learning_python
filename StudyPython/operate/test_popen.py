#!/usr/bin/env python
# coding:utf8

import os
import commands

#f_r = os.popen('top')
#try:
#    while True:
#        print f_r.next()
#        #print '-'*50
#        #f_r.seek(0)
#except:
#    pass
#finally:
#    f_r.close()

print commands.getstatusoutput('ps aux')[1]
