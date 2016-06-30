#!/usr/bin/python
#coding:UTF-8
##!/bin/sh

import os
import sys
import util
import platform

def servicetemplate(startcmd,stopcmd):
    template = """#!/bin/bash
###########################
#Licensed Materials - Property of HUADI
###########################

# chkconfig: 2345 99 50
# description: CE Service Series

### BEGIN INIT INFO
# Provides:ce
# Required-Start:$all
# Required-Stop:
# Default-Start:2 3 4 5
# Default-Stop:0 1 6
# X-Interactive:false
# Short-Description: Start or stop the CE Service Series.
### END INIT INFO

case "$1" in
    start)
            %s
    ;;
    stop)
            %s
    ;;
esac

exit $?
"""
    if startcmd == None: startcmd = 'sleep 1'
    if stopcmd == None: stopcmd = 'sleep 1'
    
    return template %(startcmd,stopcmd)
    

def createService():
    startcmd = 'sh /opt/huadi/ce/CE.sh'
    stopcmd = None
    content = servicetemplate(startcmd,stopcmd)
    filename = '/etc/init.d/ce'
    util.writefile(filename, content)
    os.system('chmod +x ' + filename)
    if 'debian' in platform.platform().lower() or 'ubuntu' in platform.platform().lower():
        os.system('update-rc.d ce defaults 99')
    else:
        os.system('chkconfig --add ce')
        
def removeService():
    if 'debian' in platform.platform().lower() or 'ubuntu' in platform.platform().lower():
        os.system('update-rc.d -f ce remove')
    else:
        os.system('chkconfig --del ce')
    os.system('rm -f /etc/init.d/ce')

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1].strip() == '-u':
        removeService()
    else:
        createService()