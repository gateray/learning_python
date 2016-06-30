#!/usr/bin/env python
# coding: utf-8

import glob

#将一个路径通配符解析为路径列表
paths = glob.glob('./*.py')
print(paths)

#将一个路径通配符解析为一个生成器对象,用于路径迭代
ipaths = glob.iglob('./*.py')
for path in ipaths:
    print(path)