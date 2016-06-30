#!/usr/bin/env python
#

import os
import os.path

#os.rename('test.txt.bak','test.txt')
pwd = os.getcwd()
print os.listdir(pwd)
for name in os.listdir(pwd):
    print os.path.join(pwd,name)
