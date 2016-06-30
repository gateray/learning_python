#!/usr/bin/env python
# coding: utf-8

import tarfile

# 解压tar文件中的某个文件子集,利用生成器的功能, members是一个TarInfo对象的列表
import os
def py_files(tar):
    for tarinfo in tar:
        if os.path.splitext(tarinfo.name)[1] == ".py":
            yield tarinfo

tar = tarfile.open("sample.tar.gz")
tar.extractall(members=py_files(tar))
tar.close()
