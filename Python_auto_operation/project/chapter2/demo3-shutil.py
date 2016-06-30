#!/usr/bin/env python
# coding: utf-8

import shutil
import filecmp
import os.path
import os

class Compare2file:
    def __init__(self, path1, path2):
        self.diffset = set()
        self.dirobj = filecmp.dircmp(path1, path2)

    def _getdiff(self,dirobj):
        diff_list = dirobj.left_only + dirobj.diff_files
        for file in diff_list:
            self.diffset.add(os.path.join(dirobj.left,file))
        for subdirobj in dirobj.subdirs.itervalues():
            self._getdiff(subdirobj)
    @property
    def result(self):
        self._getdiff(self.dirobj)
        return self.diffset

class SynchronizeFiles:
    def __init__(self, path1, path2):
        self.path1 = path1
        self.path2 = path2
        self.comp = Compare2file(path1, path2)
    def synchronize(self):
        diff_set = self.comp.result
        print(diff_set)
        for file in diff_set:
            tgtfile = file.replace(self.path1,self.path2,1)
            if os.path.isdir(file):
                shutil.copytree(file,dst=tgtfile)
            else:
                shutil.copy2(file,tgtfile)

if __name__ == '__main__':
    sf = SynchronizeFiles('dir1','dir2')
    sf.synchronize()