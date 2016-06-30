#!/usr/bin/env python
# coding: utf-8

import difflib
import sys

try:
    textfile1 = sys.argv[1]
    textfile2 = sys.argv[2]
except Exception as e:
    print("Error:"+str(e))
    print("Usage: {} filename1 filename2".format(sys.argv[0]))
    sys.exit()

def readfile(filename):
    with open(filename) as f:
        text = f.readlines()
    return text

text1_lines = readfile(textfile1)
text2_lines = readfile(textfile2)

d = difflib.Differ()
diff = d.compare(text1_lines,text2_lines)
print('\n'.join(list(diff)))


d = difflib.HtmlDiff()
print(d.make_file(text1_lines, text2_lines))
