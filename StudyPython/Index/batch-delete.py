#!/usr/bin/env python
# coding: utf8

import re
import os

htmldir='/data/html/bd/publish'
imagedir='/data/html/bd/nfs_share'

with open('sql.txt','r') as f:
    for line in f:
        arr = line.split()
        htmlfile =  arr[0].strip('"')
        imagefile = re.search(r'^http://.*?(?=/)(.*)$',arr[1].strip('"')).group(1)
        path1=htmldir+htmlfile
        path2=imagedir+imagefile
        try:
            print 'path1: %s'%path1
            print 'path2: %s'%path2
            os.remove(path1)
            os.remove(path2)
        except Exception as e:
            print e




