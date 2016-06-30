#!/usr/bin/env python
# coding: utf-8

import dns.resolver

#domain = raw_input("Please input an domain: ")
domain="www.bingodu.com"
answer = dns.resolver.query(domain, 'A')
for A in answer:
    print(A.address)

"""
Please input an domain: www.bingodu.com
183.136.217.82
222.186.17.98
222.186.17.96
222.186.17.99
222.186.17.97
"""
