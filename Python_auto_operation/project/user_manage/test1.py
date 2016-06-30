import os

out = os.popen("sudo su root -c 'cat >>/tmp/haha.txt<<EOF\n"
               "line1.\n"
               "line2.\n"
               "EOF\n'")
