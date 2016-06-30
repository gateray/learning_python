#!/usr/bin/env python
# coding: utf-8

import subprocess

'用于获取命令返回的状态码,错误的命令不会抛出异常'
status = subprocess.call("ls -l /tmp",shell=True)
print(status)
print(status)