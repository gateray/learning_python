#!/usr/bin/env python
# coding: utf-8

import dns.resolver
import os
import httplib

appdomain = "www.keke289.com"
iplist = []

def get_iplist(domain):
    try:
        answer = dns.resolver.query(domain, 'A')
    except Exception as e:
        print("dns resolver error: {}".format(str(e)))
        return False
    for A in answer:
        iplist.append(A.address)
    return True

def checkresponse(ip, port):
    response = ""
    http = httplib.HTTPConnection(ip,port=80,timeout=5)
    try:
        http.request("GET","/",headers={"Host":appdomain})
        response = http.getresponse().read(15)
        #response = http.getresponse()
    finally:
        # pass
        if response.lower() == "<!doctype html>":
            print(ip + " [OK]")
        else:
            print(response)

if __name__ == '__main__':
    if get_iplist(appdomain):
        for ip in iplist:
            checkresponse(ip,80)
    else:
        print("dns resolver error.")

