#!/usr/bin/env python
# coding: utf-8

import subprocess

'用于取代shell中的管道'
p1 = subprocess.Popen(['cat','/etc/passwd'],stdout=subprocess.PIPE)
p2 = subprocess.Popen(['grep','^root'],stdin=p1.stdout,stdout=subprocess.PIPE)
p1.stdout.close()
print(p2.communicate()[0])

'第二种实现方法'
output = subprocess.check_output("cat /etc/passwd | grep '^root'",shell=True)
print(output)
