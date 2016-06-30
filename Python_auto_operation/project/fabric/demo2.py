#!/usr/bin/env python
# coding: utf-8

from fabric.api import *
from fabric.context_managers import *
from fabric.contrib.console import confirm
import os.path
"""
fab -f demo2.py go
"""

env.user = "vagrant"
env.password = "vagrant"
env.hosts = ["192.168.10.31", "192.168.10.32", "192.168.10.33"]

lpath = "/home/gateray/src/mongodb/mongodb-linux-x86_64-3.0.8.tgz"
rpath = "/tmp/install"

@task
def put_task():
    run("mkdir -p /tmp/install")
    with settings(warn_only=True):    #put上传出现异常时继续执行,非终止
        result = put(lpath,rpath)
    if result.failed and not confirm("put file fail, continue[y/n]?"):   #出现异常时让用户选择是否继续
        abort("aborting file put task!")

@task
def run_task():
    with cd("/tmp/install"):
        run("tar xf "+ os.path.basename(lpath)+" -C /home/vagrant")

@task
def go():
    put_task()
    run_task()