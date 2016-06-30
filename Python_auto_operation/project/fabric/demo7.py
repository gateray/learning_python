#!/usr/bin/env python
# coding: utf-8

from fabric.api import *

def task1():
    env.hosts = ["192.168.10.31","192.168.10.32"]
    env.user = "vagrant"
    env.password = "vagrant"

    with settings(warn_only=True):
        run('echo "hello world."')
    with settings(warn_only=True):
        run('echo "hello new world."')


#
# def task2():
#     env.hosts = ["192.168.10.32",]