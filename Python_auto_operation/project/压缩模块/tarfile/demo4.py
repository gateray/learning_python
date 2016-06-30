#!/usr/bin/env python
# coding: utf-8

import tarfile

#读取一个gzip tar包显示其成员信息
tar = tarfile.open("sample.tar.gz","r:gz")
for tarinfo in tar:
    print("{} is {} bytes in size and is".format(tarinfo.name, tarinfo.size)),
    if tarinfo.isreg():
        print("a regular file.")
    elif tarinfo.isdir():
        print("a directory.")
    else:
        print("something else.")
tar.close()