#!/usr/bin/python
#coding:UTF_8
import os
import commands
import re
import setNetInfo
import util

logger = util.get_logger()

if os.path.exists('/dev/cdrom'):
    status,output = commands.getstatusoutput('mount /dev/cdrom /mnt')
    if status != 0:
        logger.error('mount cd is faile:%s',output)
    else:
        logger.info('cd drive mount succeed')
else:
    block = '/sys/block'
    for b in os.listdir(block):
        if (re.match("^x", b) or re.match("^s", b)) and os.path.exists('/dev/'+b):
            status = os.system('mount /dev/'+b+' /mnt &> /dev/null')
            if status == 0: 
                if os.path.isfile('/mnt/ovf-env.xml'):
                    logger.info('cd drive mount succeed')
                    break
                else:
                    os.system('umount /mnt')

fileDir = '/opt/huadi/ce/CR'   
if os.path.isfile('/mnt/ovf-env.xml'):
    if not os.path.exists(fileDir):
        os.makedirs(fileDir)
    status,output = commands.getstatusoutput('cp /mnt/ovf-env.xml '+fileDir)
    if status != 0:
        logger.error('cp ovf-env.xml is faile:%s',output)
    commands.getstatusoutput('umount /mnt')
    setNetInfo.setNetConf(fileDir)
else:
    logger.error('ovf-env.xml not found')