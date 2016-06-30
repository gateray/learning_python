#!/usr/bin/env python
# coding: utf-8

import zipfile

"""
需要对某个目录进行压缩时,需要递归该目录下所有文件和目录,然后调用write()来添加到zip包中
"""
#创建一个zip压缩文件
# zf = zipfile.ZipFile("sample.zip",'w')
# files = ["dir1", 'file.txt']
# for file in files:
#     zf.write(file)
# zf.close()

#往zip包中追加文件
# with zipfile.ZipFile("sample.zip","a") as zf:
#     zf.write('file.py')

#解压文件
with zipfile.ZipFile("sample.zip") as zf:
    zf.extractall(path="/tmp")

