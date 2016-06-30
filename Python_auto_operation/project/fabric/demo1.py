#!/usr/bin/env python
# coding: utf-8

from fabric.api import *
"""
fab -f demo1.py go
"""

env.user = "vagrant"
env.hosts = ["192.168.10.31", "192.168.10.32", "192.168.10.33"]
env.password = "vagrant"

@runs_once           #该函数至执行一次
def input_raw():
    return prompt("please input directory name:", default="/home/vagrant")

def worktask(dirname):
    run("ls -l "+dirname)

@task      #fab命令只能直接调用被该装饰器标识的函数
def go():
    getdirname = input_raw()
    worktask(getdirname)
