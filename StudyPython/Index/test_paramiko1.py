#!/usr/bin/env python
# coding:utf8

import paramiko

iplist = (
          '10.1.12.2',
          '10.1.12.11',
          '10.1.12.199',
          )
username='root'
password='Augalkfaufl@1'

def do_ssh(ip):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(ip,22,username,password,timeout=300)
        '''
        useradd -d /temp back
        echo 'back' | passwd --stdin back
        echo 'back  ALL=NOPASSWD:    /bin/chown,/bin/chmod,/bin/chgrp,/bin/rm,/bin/mkdir,/bin/mv,/bin/cp' >> /etc/sudoers
        '''
    except Exception,e:
        print 'ip: %s, error: %s'%(ip,e)
        return
    f = file('command.txt')
    for cmd in f:
        if cmd.startswith('#'): continue
        print 'execute command: %s' %cmd
        stdin,stdout,stderr = ssh.exec_command(cmd.strip())
        out = stdout.read()
        err = stderr.read()
        if err:
            print 'Warning or Error: \n%s' %err
        if out:
            print 'Result: \n%s' %out
    f.close()
    ssh.close()

print '-'*10 + 'start' + '-'*10
for ip in iplist:
    print ip + ':'
    do_ssh(ip)
print '-'*10 + 'end' + '-'*10