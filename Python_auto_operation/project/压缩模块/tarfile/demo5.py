#!/usr/bin/env python
# coding: utf-8

import tarfile
import glob

#创建gzip压缩tar时,重置文件的属主和属组
def reset(tarinfo):
    tarinfo.uid = tarinfo.gid = 0
    tarinfo.uname = tarinfo.gname = "root"
    return tarinfo
tar = tarfile.open("sample.tar.bz2","w:bz2")
for file in glob.iglob("*.py"):
    tar.add(file,filter=reset)
for tarinfo in tar:
    print(" ".join([tarinfo.name, str(tarinfo.uid), str(tarinfo.gid)]))
