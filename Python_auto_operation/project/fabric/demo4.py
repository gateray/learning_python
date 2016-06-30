#!/usr/bin/env python
# coding: utf-8

from fabric.api import *


env.roledefs = {'httpd': ['192.168.10.31', '192.168.10.32'], 'mysql': ['192.168.10.33',]}
env.user = "vagrant"
env.password = "vagrant"

@roles("httpd")
def a():
    out = run("cat /etc/passwd")
    print out,
@roles("mysql")
def b():
    out = local("head -1 /etc/passwd",capture=True)
    print(type(out.stdout))
    print(out.stdout)

def play():
    execute(a)
    execute(b)
