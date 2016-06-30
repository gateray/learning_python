#!/usr/bin/python
#coding:UTF_8
#解析XML

import os
import util
import platform

if platform.python_version() < '2.5':
    import elementtree.ElementTree as ET
else:
    import xml.etree.ElementTree as ET

IP4_NETMASK=''
IP4_GETEWAY=''
IP4_ADRESS=''
IP4_DHCP=''
IP6_GETEWAY=''
IP6_ADRESS=''
IP6_AUTOCONF=''

DOMAINAME=''
HOSTNAME=''
MAC=''
LICENSE=''
TIMEZONE=''
DNS=''

logger = util.get_logger()

def load_xml_file(xmlFile):
    if os.path.isfile(xmlFile):
        root = ET.parse(xmlFile)
        all_pro = root.findall('PropertySection')
        #遍历list节点的子元素
        for pro in all_pro:
            for child in pro.getchildren():
                if child.get('key').strip() == 'com.huadi.ovf.wce.adapter.networking.ipv4addresses.1':
                    global IP4_ADRESS
                    IP4_ADRESS = child.get('value').strip()
                    logger.info('ovf_enf.xml ip4_address:'+IP4_ADRESS)
                elif child.get('key').strip() == 'com.huadi.ovf.wce.adapter.networking.ipv4netmasks.1':
                    global IP4_NETMASK
                    IP4_NETMASK = child.get('value').strip()
                    logger.info('ovf_enf.xml ip4_NETMASK:'+IP4_NETMASK)
                elif child.get('key').strip() == 'com.huadi.ovf.wce.system.networking.ipv4defaultgateway':
                    global IP4_GETEWAY
                    IP4_GETEWAY = child.get('value').strip()
                    logger.info('ovf_enf.xml ip4_GETEWAY:'+IP4_GETEWAY)
                elif child.get('key').strip() == 'com.huadi.ovf.wce.adapter.networking.usedhcpv4.1':
                    global IP4_DHCP
                    IP4_DHCP = child.get('value').strip()
                    logger.info('ovf_enf.xml ip4_DHCP:'+IP4_DHCP)
                elif child.get('key').strip() == 'com.huadi.ovf.wce.adapter.networking.useipv6autoconf.1':
                    global IP6_AUTOCONF
                    IP6_AUTOCONF = child.get('value').strip()
                    logger.info('ovf_enf.xml ip6_AUTOCONF:'+IP6_AUTOCONF)
                elif child.get('key').strip() == 'com.huadi.ovf.wce.adapter.networking.ipv6addresses.1':
                    global IP6_ADRESS
                    IP6_ADRESS = child.get('value').strip()
                    logger.info('ovf_enf.xml ip6_ADRESS:'+IP6_ADRESS)
                elif child.get('key').strip() == 'com.huadi.ovf.wce.adapter.networking.ipv6gateways.1':
                    global IP6_GETEWAY
                    IP6_GETEWAY = child.get('value').strip()
                    logger.info('ovf_enf.xml ip6_GETEWAY:'+IP6_GETEWAY)
                elif child.get('key').strip() == 'com.huadi.ovf.wce.system.networking.domainname':
                    global DOMAINAME
                    DOMAINAME = child.get('value').strip()
                    logger.info('ovf_enf.xml DOMAINAME:'+DOMAINAME)
                elif child.get('key').strip() == 'com.huadi.ovf.wce.system.networking.hostname':
                    global HOSTNAME
                    HOSTNAME = child.get('value').strip()
                    logger.info('ovf_enf.xml HOSTNAME:'+HOSTNAME)
                elif child.get('key').strip() == 'com.huadi.ovf.wce.adapter.networking.mac.1':
                    global MAC
                    MAC = child.get('value').strip()
                    logger.info('ovf_enf.xml MAC:'+MAC)
                elif child.get('key').strip() == 'com.huadi.ovf.wce.system.networking.dnsIPaddresses':
                    global DNS
                    DNS = child.get('value').strip()
                    logger.info('ovf_enf.xml DNS:'+DNS)
                elif child.get('key').strip() == 'com.huadi.ovf.wce.system.license':
                    global LICENSE
                    LICENSE = child.get('value').strip()
                    logger.info('ovf_enf.xml LICENSE:'+LICENSE)
                elif child.get('key').strip() == 'com.huadi.ovf.wce.system.timezone':
                    global TIMEZONE
                    TIMEZONE = child.get('value').strip()
                    logger.info('ovf_enf.xml TIMEZONE:'+TIMEZONE)
                else:
                    pass
    else:
        logger.error('xml file is not exits:'+xmlFile)
