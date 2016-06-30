#!/usr/bin/env python
# coding: utf-8

from httplib2 import Http
import json
import argparse
import os
import sys
from zabbixutils import ZabbixUtil

class RabbitAPI:
    def __init__(self,host,port=15672,username='guest',password='guest'):
        self.host = host
        self.hostname = os.popen("hostname").read().strip()
        self.port = port
        self.urlprefix= "http://"+self.host+":"+str(self.port)
        self.username = username
        self.password = password
        self.httpClient = Http()
        self.httpClient.add_credentials(self.username,self.password)

    def getResources(self,path,method="GET",body=None,header={}):
        resp, content = self.httpClient.request(self.urlprefix+path,method,body,header)
        return json.loads(content)

    def list_nodes(self):
        """
        api-sample:
            nodes:
            [{"name":"rabbit@rabbitmq"}]
        :return:
        """
        nodes = self.getResources("/api/nodes?columns=name")
        return ZabbixUtil.convert2marcojson({"name":"{#NODENAME}"},nodes)

    def list_vhosts(self):
        """
        api-sample:
            vhosts:
            [{"name":"/"}]
        :return:
        """
        vhosts = self.getResources("/api/vhosts?columns=name")
        return ZabbixUtil.convert2marcojson({"name":"{#VHOSTNAME}"},vhosts)

    def list_queues(self):
        """
        api-sample:
            queues:
            [{"name":"task_queue","vhost":"/","node":"rabbit@rabbitmq"}]
        :return:{"data": [{"{#QUEUENAME}":"task_queue","{#VHOSTNAME}":"/","{#NODENAME}":"rabbit@rabbitmq"},]}
        """
        queues = self.getResources("/api/queues?columns=node,vhost,name")
        return ZabbixUtil.convert2marcojson({"name":"{#QUEUENAME}",
                                             "vhost":"{#VHOSTNAME}",
                                             "node":"{#NODENAME}"},queues)

    def check_queue(self,queue_name,item,vhost_name="/",node_name=None):
        """
        api-sample:
            queues_info:
            [
                {
                    "messages":0,
                    "messages_ready":0,
                    "messages_unacknowledged":0,
                    "name":"task_queue",
                    "vhost":"/",
                    "node":"rabbit@rabbitmq"
                },
            ]
        :param queue_name:
        :param item:
        :param vhost_name:
        :return: string of item
        """
        if not node_name: node_name="rabbit@"+self.hostname
        queues_info = self.getResources("/api/queues?columns=node,vhost,name,"
                                        "messages,"
                                        "messages_ready,"
                                        "messages_unacknowledged")
        return [ queue[item] for queue in queues_info if queue["vhost"] == vhost_name
                 and queue["name"] == queue_name and queue["node"] == node_name ][0]

    def check_node(self,item, node_name=None):
        """
        api-sample:
            nodes_info:
            [
                {
                    u'proc_total': 1048576,
                    u'proc_used': 812,
                    u'sockets_total': 829,
                    u'fd_used': 79,
                    u'disk_free_limit': 50000000,
                    u'mem_used': 77721056,
                    u'disk_free': 49484562432,
                    u'mem_limit': 1446359859,
                    u'sockets_used': 57,
                    u'fd_total': 1024,
                    u'name': u'rabbit@AZStageLA01'
                },
            ]
        :param node_name:
        :param item:
        :return:
        """
        if not node_name: node_name="rabbit@"+self.hostname
        nodes_info = self.getResources("/api/nodes?columns=name,"
                                           "disk_free,disk_free_limit,"
                                           "fd_used,fd_total,"
                                           "mem_used,mem_limit,"
                                           "proc_used,proc_total,"
                                           "sockets_used,sockets_total")
        return [ node[item] for node in nodes_info if node["name"] == node_name ][0]

    def check_overview(self,item):
        """
        api-sample:
            overview info:
            {
                u'node': u'rabbit@AZStageLA01',
                u'object_totals': {
                    u'connections': 55,
                    u'channels': 55,
                    u'queues': 12,
                    u'consumers': 81,
                    u'exchanges': 22
                },
                u'queue_totals': {
                    u'messages': 0,
                    u'messages_unacknowledged': 0,
                    u'messages_ready': 0
                }
            }
        :param item:
        :return:
        """
        #item="object_totals.connections"
        overview = self.getResources("/api/overview?columns=node,"
                                          "queue_totals.messages,"
                                          "queue_totals.messages_ready,"
                                          "queue_totals.messages_unacknowledged,"
                                          "object_totals.connections,"
                                          "object_totals.channels,"
                                          "object_totals.queues,"
                                          "object_totals.consumers,"
                                          "object_totals.exchanges")
        k1,k2 = item.split(".")
        return overview[k1][k2]

if __name__ == "__main__":
    #ra = RabbitAPI("azstage.chinacloudapp.cn",username="admin",password="go4xpggo4xpg")
    ra = RabbitAPI("192.168.10.28")
    #print ra.check_queue("aos_rt_data_2","messages_ready")
    parser = argparse.ArgumentParser(description="The Program is useful to get the RabbitMQ monitor items.")
    parser.add_argument("-N","--node",nargs="?",help="specify a node name",metavar="NONENAME",const="rabbit@"+ra.hostname)
    parser.add_argument("-Q","--queue",help="specify a queue name",metavar="QUEUENAME")
    parser.add_argument("-d","--vhost",nargs="?", help="specify a vhost name",metavar="VHOSTNAME", const="/")
    parser.add_argument("-k", "--item",help="specify a monitor item",metavar="MONITORITEM")
    parser.add_argument("-l", "--list", choices=["queues","vhosts","nodes"],help="list the queues, vhost or nodes")
    ns = parser.parse_args(sys.argv[1:])
    if ns.queue and ns.item:
        node = "rabbit@"+ra.hostname if not ns.node else ns.node
        vhost = "/" if not ns.vhost else ns.vhost
        print(ra.check_queue(ns.queue,ns.item,vhost_name=vhost,node_name=node))
    elif ns.node and ns.item:
        print(ra.check_node(ns.item,node_name=ns.node))
    elif ns.list:
        print(getattr(ra,"list_"+ns.list)())
    elif ns.item:
        print(ra.check_overview(ns.item))
    else:
        parser.print_help()
