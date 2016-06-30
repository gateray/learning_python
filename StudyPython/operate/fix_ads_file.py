#!/usr/bin/env python
# coding: utf8

text='''
51,null,223.96.148.1,DD9FF55FB71090F5E04AD41203320CC0,1,6,20150812104848,1000001,山东省,德州市,null,null
50,null,223.96.148.1,DD9FF55FB71090F5E04AD41203320CC0,1,6,20150812104848,1000001,山东省,德州市,null,null
52,null,223.96.148.1,DD9FF55FB71090F5E04AD41203320CC0,1,10,20150812104848,1000001,山东省,德州市,null,null
27,null,183.6.158.198,1000001,2,9,20150812104915,16032D6C8C350F587621AE18C7FA277C,广东省,广州市,null,null
51,null,223.96.148.1,DD9FF55FB71090F5E04AD41203320CC0,1,6,20150812104848,1000001,山东省,德州市,null,null
50,null,223.96.148.1,DD9FF55FB71090F5E04AD41203320CC0,1,6,20150812104848,1000001,山东省,德州市,null,null
52,null,223.96.148.1,DD9FF55FB71090F5E04AD41203320CC0,1,10,20150812104848,1000001,山东省,德州市,null,null
51,null,223.96.148.1,DD9FF55FB71090F5E04AD41203320CC0,1,6,20150812104848,1000001,山东省,德州市,null,null
27,null,183.6.158.198,1000001,2,9,20150812104915,16032D6C8C350F587621AE18C7FA277C,广东省,广州市,null,null
50,null,223.96.148.1,DD9FF55FB71090F5E04AD41203320CC0,1,6,20150812104848,1000001,山东省,德州市,null,null
52,null,223.96.148.1,DD9FF55FB71090F5E04AD41203320CC0,1,10,20150812104848,1000001,山东省,德州市,null,null
27,null,183.6.158.198,1000001,2,9,20150812104915,16032D6C8C350F587621AE18C7FA277C,广东省,广州市,null,null
51,null,223.96.148.1,DD9FF55FB71090F5E04AD41203320CC0,1,6,20150812104848,1000001,山东省,德州市,null,null'''

'''
for line in text.split('\n'):
    fields = line.split(',')
    if len(line)==0 or len(fields) > 12 or len(fields[7])>10: continue
    print line
'''

import fileinput
import os
import os.path

def sed(paths):
    for line in fileinput.input(paths,inplace=1):
        fields = line.split(',')
        if len(fields) != 12 or len(fields[7])>10:
            line.replace(line,'')
            continue
        print(line),

if __name__ == '__main__':
    paths = []
    dir = os.path.join(os.curdir,'a')
    dir = os.path.abspath(dir)
    for file in os.listdir(dir):
        file = os.path.join(dir,file)
        if os.path.isfile(file):
            paths.append(file)
    sed(paths)
