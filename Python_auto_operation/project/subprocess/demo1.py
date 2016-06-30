#!/usr/bin/env python
# coding: utf-8

'用来取代output=`ls -l /tmp`'
import subprocess
try:
    output = subprocess.check_output(['ls','-l','/tmp'])
    print(output)
except subprocess.CalledProcessError as e:
    pass
