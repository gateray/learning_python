#!/usr/bin/python
#coding:UTF-8

import os
import re
import subprocess
import string
import commands
import platform
import util
import parseXML as xml

logger = util.get_logger()

def execute(cmd):
    logger.info("start execute cmd:"+cmd)
    status,output = commands.getstatusoutput(cmd)
    logger.debug("execute cmd is result: %s",status)
    logger.debug("execute cmd is output: " + output)
    if status != 0:
        raise Exception,'command execute is faile:'+cmd
    return status,output

def echo(info,destFile):
    logger.info("echo is start:info="+info+"--destFile"+destFile)
    execute('echo "'+info+'" >> '+destFile)
    logger.info("echo is success")
    
def getInterface():
    interface = 'eth0'
    logger.info("start get interface")
    if len(xml.MAC) > 0:
        logger.info("get interface by mac:%s",xml.MAC)
        nics = getNics()
        for index, adapter in enumerate(nics):
            if xml.MAC.upper() == nics[adapter].upper():
                interface = adapter
                break
    logger.info("get interface sucess:%s",interface)
    return interface

def getNics():
    logger.info("start get Nics")
    p1 = subprocess.Popen(['/sbin/ifconfig', '-a'], stdout=subprocess.PIPE)
    p2 = subprocess.Popen(["grep", "^eth"], stdin=p1.stdout, stdout=subprocess.PIPE)
    p1.stdout.close()  # Allow p1 to receive a SIGPIPE if p2 exits.
    output = p2.communicate()[0]

    lines = string.split(output, "\n")

    nics = {}
    for line in lines:
        m = re.search('(eth\d).*HWaddr\s(\w{2}\:\w{2}\:\w{2}\:\w{2}\:\w{2}\:\w{2})', line)
        if m != None:
            nics[m.group(1)] = m.group(2).upper()
    logger.info("get Nics sucess:%s",nics)
    return nics

def setUbuntu(interface):
    hostNameFile = "/etc/hostname"
    inetFile = "/etc/network/interfaces"
    dnsFile = "/etc/resolv.conf"
    
    execute('echo auto '+interface+' > '+inetFile)
    echo('iface '+interface+' inet static',inetFile)
    if len(xml.IP4_ADRESS)>0:
        echo('address '+xml.IP4_ADRESS,inetFile)
    if len(xml.IP4_GETEWAY)>0:
        echo('gateway '+xml.IP4_GETEWAY,inetFile)
    if len(xml.IP4_NETMASK)>0:
        echo('netmask '+xml.IP4_NETMASK,inetFile)
    if len(xml.IP6_ADRESS)>0:
        echo('iface '+interface+' inet6 static',inetFile)
        echo('address '+xml.IP6_ADRESS,inetFile)
        echo('netmask 64',inetFile)
    if len(xml.IP6_GETEWAY)>0:
        echo('gateway '+xml.IP6_GETEWAY,inetFile)
    if len(xml.DNS)>0:
        execute('echo nameserver '+ xml.DNS +' > '+dnsFile)
    if len(xml.HOSTNAME)>0:
        execute('echo ' + xml.HOSTNAME +'  > '+hostNameFile)
        execute('hostname '+xml.HOSTNAME)

def setSuse(interface):
    hostNameFile = "/etc/HOSTNAME"
    inetFile = "/etc/sysconfig/network/ifcfg-"+interface
    gateWayFile = "/etc/sysconfig/network/routes"
    dnsFile = "/etc/resolv.conf"
    
    execute('echo DEVICE='+interface+' > '+inetFile)
    echo('BOOTPROTO=static',inetFile)
    echo('TYPE=Ethernet',inetFile)
    echo('STARTMODE=auto',inetFile)
    echo('ONBOOT=yes',inetFile)
    if len(xml.IP4_ADRESS)>0:
        echo('IPADDR='+xml.IP4_ADRESS,inetFile)
    if len(xml.IP4_NETMASK)>0:
        echo('NETMASK='+xml.IP4_NETMASK,inetFile)
    if len(xml.IP6_ADRESS)>0:
        echo('IPV6INIT=yes',inetFile)
        echo('LABEL_0=0',inetFile)
        echo('IPADDR_0='+xml.IP6_ADRESS,inetFile)
        echo('PREFIXLEN_0=64',inetFile)
    if len(xml.IP4_GETEWAY)>0:
        execute('echo default '+xml.IP4_GETEWAY+' - - > '+gateWayFile)
    if len(xml.IP6_GETEWAY)>0:
        if len(xml.IP4_GETEWAY)>0:
            echo('default '+xml.IP6_GETEWAY+' - -',gateWayFile)
        else:
            execute('echo default '+xml.IP6_GETEWAY+' - - > '+gateWayFile)
    if len(xml.DNS)>0:
        execute('echo nameserver '+ xml.DNS +' > '+dnsFile)
    if len(xml.HOSTNAME)>0:
        execute('echo ' + xml.HOSTNAME +'  > '+hostNameFile)
        execute('hostname '+xml.HOSTNAME)

def setRedHat(interface):
    hostNameAndGeteWayFile = "/etc/sysconfig/network"
    inetFile = "/etc/sysconfig/network-scripts/ifcfg-"+interface
    dnsFile = "/etc/resolv.conf"
    
    execute('echo DEVICE='+interface+' > '+inetFile)
    echo('BOOTPROTO=static',inetFile)
    echo('TYPE=Ethernet',inetFile)
    echo('STARTMODE=auto',inetFile)
    echo('ONBOOT=yes',inetFile)
    if len(xml.IP4_ADRESS)>0:
        echo('IPADDR='+xml.IP4_ADRESS,inetFile)
    if len(xml.IP4_NETMASK)>0:
        echo('NETMASK='+xml.IP4_NETMASK,inetFile)

    if len(xml.DNS)>0:
        execute('echo nameserver '+ xml.DNS +' > '+dnsFile)
    if len(xml.HOSTNAME)>0:
        execute('echo NETWORKING=yes > '+hostNameAndGeteWayFile)
        echo('HOSTNAME=' + xml.HOSTNAME,hostNameAndGeteWayFile)
        execute('hostname '+xml.HOSTNAME)
        if len(xml.IP4_GETEWAY)>0:
            echo('GATEWAY=' + xml.IP4_GETEWAY,hostNameAndGeteWayFile)
    elif len(xml.IP4_GETEWAY)>0:
        echo('GATEWAY='+xml.IP4_GETEWAY,inetFile)
    else:
        pass
    if len(xml.IP6_ADRESS)>0:
        echo('IPV6INIT=yes',inetFile)
        echo('IPV6_AUTOCONFI=no',inetFile)
        echo('IPV6ADDR='+xml.IP6_ADRESS,inetFile)
        echo('NETWORKING_IPV6=yes',hostNameAndGeteWayFile)
    if len(xml.IP6_GETEWAY)>0:
        echo('IPV6_DEFAULTGW=' + xml.IP6_GETEWAY,hostNameAndGeteWayFile)
    
    
def setNetConf(fileDir):       
    logger.info("setNetConf is start")  
    result = 0
    
    #解析XML
    xml.load_xml_file(fileDir+'/ovf-env.xml')
    #獲取網卡
    interface = getInterface()
    
    try:
        if 'debian' in platform.platform().lower() or 'ubuntu' in platform.platform().lower():
            setUbuntu(interface)
            logger.info('restart networking')
            execute('/etc/init.d/networking restart')
        elif 'suse' in platform.platform().lower():
            setSuse(interface)
            logger.info('restart networking')
            execute('/etc/init.d/network restart')
        else:
            setRedHat(interface)
            logger.info('restart networking')
            execute('/etc/init.d/network restart')
        logger.info("setInfo is success")
    except Exception,e:
        exception = e
        result = 1
        logger.error("############setNetConf faile############:%s",e)
    return result
