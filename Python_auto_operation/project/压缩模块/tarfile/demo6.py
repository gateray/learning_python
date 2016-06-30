#!/usr/bin/env python
# coding: utf-8

import tarfile

#解压tar包中的指定文件到/tmp目录,member可以是一个文件名或TarInfo对象
tar = tarfile.open("sample.tar.gz","r:gz")
tar.extract(member="dir1/file1.py",path='/tmp')
tar.close()