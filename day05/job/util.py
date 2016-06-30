#!/usr/bin/env python
# coding: utf8

import json
import commands
import os.path as op

__config = {}

def loadconfig(path=op.join(op.dirname(op.abspath(__file__)),'config.json')):
    global __config
    if not __config:
        with open(path,'r') as f:
            __config = json.load(f)
        print __config
    return __config

