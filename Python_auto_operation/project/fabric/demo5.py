#!/usr/bin/env python
# coding: utf-8

from fabric.api import *

def useradd(username,uid,groupname,e_gids):
    """
    create a user. required args: (username,uid,groupname,e_gids)
    """
    print("username: "+username)
    print("uid: " + uid)
    print("groupname: " + groupname)
    print("e_gids: " + e_gids)
