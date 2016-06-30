#!/usr/bin/python
#coding:UTF-8
#工具類

import os
import logging
from logging.handlers import RotatingFileHandler

#獲取LOG
logger = None
def get_logger(logfile='/opt/huadi/ce/log/ce.log',
            level=logging.NOTSET):
    mkdirs(logfile)    
    global logger
    if logger == None:
        logger = logging.getLogger()
        Rthandler = RotatingFileHandler(logfile, maxBytes=5*1024*1024,backupCount=5)
        formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
        Rthandler.setFormatter(formatter)
        logger.addHandler(Rthandler)
        logger.setLevel(level)
    return logger
    
def writefile(filename, content, append=False):
    """OS-independent write file API."""
    mkdirs(filename)
    f = None
    if append:
        f = open(filename, 'a')
    else:
        f = open(filename, 'w')
    f.write(content)
    f.close()

def mkdirs(filename):
    pathname = os.path.dirname(filename)
    if os.path.exists(pathname) == False:
        # Make directories
        os.makedirs(pathname) 