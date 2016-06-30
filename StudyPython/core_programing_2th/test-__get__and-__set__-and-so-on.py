#!/usr/bin/env python

import os
import pickle

class FileDescr(object):
    saved = []
    def __init__(self, name=None):
       self.name = name
    def __get__(self, obj, typ=None):
        print '----------get----------%s--------------------' %self.name
        if self.name not in FileDescr.saved:
            raise AttributeError, \
             "%r used before assignment" % self.name
        try:
            f = open(self.name, 'r')
            val = pickle.load(f)
            f.close()
            return val
        except (pickle.UnpicklingError, IOError,
                    EOFError, AttributeError,ImportError, IndexError), e:
            raise AttributeError, \
                "could not read %r: %s" % self.name
    def __set__(self, obj, val):
        f = open(self.name, 'w')
        print '------------set--------%s--------------------' % self.name
        try:
            pickle.dump(val, f)
            FileDescr.saved.append(self.name)
        except (TypeError, pickle.PicklingError), e:
            raise AttributeError , "could not pickle %r" % self.name
        finally:
            f.close()

    def __delete__(self, obj):
        try:
            os.unlink(self.name)
            FileDescr.saved.remove(self.name)
        except (OSError, ValueError), e:
            pass

class MyFileVarClass:
    foo = FileDescr('foo')
    bar = FileDescr('bar')

mfvc = MyFileVarClass()
# print MyFileVarClass.foo  ##error
# print mfvc.bar  ##error
MyFileVarClass.foo = 32
# mfvc.bar = 'diaoni'
print MyFileVarClass.foo
