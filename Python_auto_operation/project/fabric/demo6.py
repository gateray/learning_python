#!/usr/bin/env python
# coding: utf-8

from fabric.api import *

class User:
    def __init__(self,username):
        print("create a user: %s"%username)
    def callme(self):
        print("call a user")
