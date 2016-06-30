#!/usr/bin/env python
# coding: utf-8

import tarfile

#创建一个无压缩的tar包
import os
with tarfile.open("sample.tar","w") as tar:
    for name in os.listdir("."):
        tar.add(name)
