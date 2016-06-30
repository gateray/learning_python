#!/usr/bin/env python
# coding: utf-8

class ZabbixUtil:
    def __init__(self):
        pass
    @staticmethod
    def convert2marcojson(keymapping,init_list):
        """
        :param keymapping: {"name":"{#QUEUESNAME}","vhost":"{#VHOSTNAME}","node":"{#NODENAME}"}
        :param initlist: [{name:"queue1",vhost:"/vhost1",node:"node1"}, {name:"queue2",vhost:"/vhost2",node:"node2"}]
        :return: "{"data":[
                             {"{#QUEUESNAME}":"queue1","{#VHOSTNAME}":"/vhost1","{#NODENAME}":"node1"},
                             {"{#QUEUESNAME}":"queue2","{#VHOSTNAME}":"/vhost2","{#NODENAME}":"node2"}
                          ]
                  }"
        """
        import json
        new_list = []
        for ele in init_list:
            new_list.append(dict([(v,ele[k]) for k,v in keymapping.items()]))
        return json.dumps({"data":new_list})


