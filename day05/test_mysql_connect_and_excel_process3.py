#!/usr/bin/env python
# coding: utf8

import MySQLdb
import sys
import time
import xlwt
import re
from xlrd import open_workbook
from xlutils.copy import copy

try:
    rb = open_workbook('6.16top100.xls')
    rs = rb.sheet_by_index(0)
    wb = copy(rb)
    ws = wb.get_sheet(0)
    conn = MySQLdb.connect('10.1.12.42', 'root', 'mysqlnhzw_2988', 'bingdu')
    cur = conn.cursor()
    for i in range(rs.nrows):
        if not i:
            ws.write(0,2,u'新闻标题')
            ws.write(0,3,u'频道ID')
            ws.write(0,4,u'频道名称')
        else:
            url = rs.cell_value(i,0)
            m = re.search(r'.*/(\d+)\.html',url)
            news_id = int(m.group(1))
            sql = 'SELECT news_title,channel FROM bd_news_details WHERE news_id=%d'%news_id
            cur.execute(sql)
            rslt = cur.fetchone()
            news_title = rslt
            print 'end'


except MySQLdb.MySQLError as e:
    print e
    conn.rollback()
except Exception as e:
    print e
