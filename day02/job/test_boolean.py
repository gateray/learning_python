#!/usr/bin/env python
#

isDirty = False

def change(flag):
    global isDirty
    isDirty = flag
    print isDirty




change(True)
print isDirty
