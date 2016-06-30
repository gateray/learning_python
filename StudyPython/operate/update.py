#!/usr/bin/python
import sys
import os
import time
import shutil
import tarfile

current_time = time.strftime("%Y%m%d_%H%M",time.localtime())
service_list = ['tomcat','wap','spider','api','management_80','timer','consumer','api.ab','consumer.ab']

if sys.argv[1] != 'backuponly':
    original_war = '/root/%s'%sys.argv[3]
    war_name = sys.argv[3]
#    backup_war = '/backup/'+original_war[0:-4]+'.'+current_time+'.war'
current_dir = os.getcwd()

if sys.argv[2] in service_list:
    service = sys.argv[2]
    service_path = '/usr/local/%s' % service
    deploy_path = '%s/webapps/ROOT' % service_path
    service_bak_path = '/backup/%s' % service

    service_stop = 'ps -ef |grep /usr/local/%s|grep -v grep|awk \'{print $2}\'|xargs kill -9' % service
    service_start = '/usr/local/%s/bin/catalina.sh start' % sys.argv[2]

    print 'Service deploy path: %s' % deploy_path
    print 'Service path: %s' % service_path
else:
    print 'service name is not correct.'
    exit()


if not os.path.isdir('%s'%service_path):
    print '%s is not deployed. check service name.'% service
    exit()


def service_restart():
    os.system(service_stop)
    time.sleep(2)
    os.system(service_start)

def tar_zip():
    if not os.path.isdir('/backup/%s'%service):
        os.mkdir('/backup/%s'%service)
    os.chdir('%s/webapps/ROOT'%service_path)
    print 'Start the zip, format gz.'
    print 'Current dir: %s'%os.getcwd()
    t = tarfile.open('/backup/%s/%s.%s.tgz'%(service, service, current_time), "w|gz")
    t.add('./')
    t.close()
    os.chdir(current_dir)

def tar_unzip():
    if '%s/%s'%(service_bak_path, sys.argv[3]):
        t = tarfile.open('%s/%s'%(service_bak_path, sys.argv[3]))
        t.extractall(deploy_path)
        t.close()
    else:
        print '%s/%s is not exists'%(service_bak_path, sys.argv[3])

def backup_(service_name):
    os.chdir(pwd)
    print 'current dir --> %s'%os.getcwd()
    if os.path.exists(service_bak_path):
        shutil.copy(original_war,service_bak_path)
        os.chdir(service_bak_path)
        os.rename(original_war,backup_war)
    else:
        os.makedirs(service_bak_path)
        shutil.copy(original_war,service_bak_path)
        os.chdir(service_bak_path)
        os.rename(original_war,backup_war)

    os.chdir('/root')


def change():
    print 'Start the update.'
    try:
        for root,dirs,files in os.walk('%s/webapps/ROOT'%service_path):
            for i in files:
                os.remove(os.path.join(root,i))
            for d in dirs:
                shutil.rmtree(os.path.join(root,d))
        if os.path.isfile(original_war):
            shutil.copy(original_war, deploy_path)
        else:
            exit()
        print original_war
        print deploy_path
        shutil.copy(original_war,deploy_path)
        os.chdir('%s/webapps/ROOT'%service_path)
        print 'Unzip path is: %s' % os.getcwd()
        os.system('unzip %s > /dev/null'%war_name)
        os.remove(war_name)
        service_restart()
    except OSError, E:
        print str(E)


def service_rollback():
    try:
        for root,dirs,files in os.walk('%s/webapps/ROOT'%service_path):
            for i in files:
                os.remove(os.path.join(root,i))
            for d in dirs:
                shutil.rmtree(os.path.join(root,d))
        tar_unzip()
    except OSError, E:
        print str(E)





if sys.argv[1] == 'update' :
    tar_zip()
    change()
elif sys.argv[1] == 'rollback':
    service_rollback()
elif sys.argv[1] == 'backuponly':
    tar_zip()
else:
    print './update.py [update|rollback] [service name] [package.war|package.tgz]'
    exit()












#if sys.argv[1] == 'spider':
#    os.system('/usr/local/tomcat/bin/catalina.sh stop')
#
#    if int(os.popen(tomcat).read()) == 0:
#       rm_olds()
#       os.sleep(1)
#       update_()
#       os.sleep(1)
#       os.system('/usr/local/tomcat/bin/catalina.sh start')
#    else:
#       os.system(kill_tomcat)
#       rm_olds()
#       update_()
#       os.system('/usr/local/tomcat/bin/catalina.sh start')
#else:
#    print 'argv[1] error.'