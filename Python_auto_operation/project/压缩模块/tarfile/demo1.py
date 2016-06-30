#!/usr/bin/env python
# coding: utf-8

import tarfile
"""
tarfile.open(tarfilename,mode),当mode为'filemode[:compression]'格式时,返回一个可迭代对象,每次迭代返回一个TarInfo对象;
当mode为'filemode[|compression]'格式时,返回的是一个stream对象,不能用于迭代并且不能只解压部分文件;
mode由一个字符串格式组成'filemode[:compression]', 默认为'r'. 以下是每种模式的说明:
mode	action
'r' or 'r:*'	打开一个压缩的tar文件,对于tar的压缩格式是透明的.=>tar xf
'r:'	打开一个无压缩的tar文件. =>tar xf
'r:gz'	打开一个gzip压缩的tar文件. =>tar xzf
'r:bz2'	打开一个bzip2压缩的tar文件. =>tar xjf
'a' or 'a:'	向一个无压缩的tar文件追加内容 =>tar rf
'w' or 'w:'	将内容写入一个无压缩的tar文件.=>tar cf
'w:gz'	将内容写入一个gzip压缩的tar文件.=>tar czf
'w:bz2'	将内容写入一个bzip2压缩的tar文件.=>tar cjf
还有另外一种基于stream的打开模式
Mode	Action
'r|*'	Open a stream of tar blocks for reading with transparent compression.
'r|'	Open a stream of uncompressed tar blocks for reading.
'r|gz'	Open a gzip compressed stream for reading.
'r|bz2'	Open a bzip2 compressed stream for reading.
'w|'	Open an uncompressed stream for writing.
'w|gz'	Open an gzip compressed stream for writing.
'w|bz2'	Open an bzip2 compressed stream for writing.
"""

#解压一个tar包到当前目录
tar = tarfile.open("sample.tar.gz")
tar.extractall()
tar.close()
