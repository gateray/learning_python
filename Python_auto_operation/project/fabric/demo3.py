#!/usr/bin/env python
# coding: utf-8

from fabric.api import *

env.hosts = ["192.168.10.31",]
env.user = "vagrant"
env.password = "vagrant"

@task
def hello():
    with settings(warn_only=True):
        rs = local("grep -c '^fuck' /etc/group || /bin/true")
        print(rs.stdout)
