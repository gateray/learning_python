#!/usr/bin/env python
# coding: utf-8

import filecmp

dir1 = "dir1"
dir2 = "dir2"
"""
dir1
├── a
│   ├── a1(内容不同)
│   └── b
│       ├── b1(内容不同)
│       ├── b2
│       └── b3
├── f1(内容不同)
├── f2
├── f3
└── f4
dir2
├── a
│   ├── a1
│   └── b
│       ├── b1
│       ├── b2
│       └── b3
├── f1
├── f2
├── f3

diff dir1 dir2
Only in dir1 : ['f4']
Only in dir2 : ['f5']
Identical files : ['f2', 'f3']
Differing files : ['f1']
Common subdirectories : ['a']

diff dir1/a dir2/a
Differing files : ['a1']
Common subdirectories : ['b']

diff dir1/a/b dir2/a/b
Identical files : ['b2', 'b3']
Differing files : ['b1']
"""
dirobj = filecmp.dircmp(dir1,dir2)

dirobj.report()
print("-"*100)
dirobj.report_partial_closure()
print("-"*100)
dirobj.report_full_closure()
print("-"*40 + "diyshow" + "-"*40)

def get_diff(dirobj):
    print("left:"+str(dirobj.left))             #left:dir1
    print("right:"+str(dirobj.right))           #right:dir2
    print("left_list:"+str(dirobj.left_list))   #left_list:['a', 'f1', 'f2', 'f3', 'f4']
    print("right_list"+str(dirobj.right_list))  #right_list['a', 'f1', 'f2', 'f3', 'f5']
    print("common:"+str(dirobj.common))         #common:['a', 'f1', 'f2', 'f3']
    print("left_only:"+str(dirobj.left_only))   #left_only:['f4']
    print("right_only:"+str(dirobj.right_only)) #right_only:['f5']
    print("common_dirs:"+str(dirobj.common_dirs))    #common_dirs:['a']
    print("common_files"+str(dirobj.common_files))   #common_files['f1', 'f2', 'f3']
    print("common_funny:"+str(dirobj.common_funny))  #common_funny:[]
    print("diff_file:"+str(dirobj.diff_files))       #diff_file:['f1']
    print("funny_files:"+str(dirobj.funny_files))     #funny_files[]
    for subdirobj in dirobj.subdirs.itervalues():
        get_diff(subdirobj)

get_diff(dirobj)