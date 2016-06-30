#!/usr/bin/env python
# coding: utf8

# import xlwt
# from datetime import datetime
#
# style0 = xlwt.easyxf('font: name Times New Roman, color-index red, bold on',
#     num_format_str='#,##0.00')
# style1 = xlwt.easyxf(num_format_str='D-MMM-YY')

# wb = xlwt.Workbook()

# ws = wb.add_sheet('A Test Sheet')

# ws.write(0, 0, 1234.56, style0)
# ws.write(1, 0, datetime.now(), style1)
# ws.write(2, 0, 1)
# ws.write(2, 1, 1)
# ws.write(2, 2, xlwt.Formula("A3+B3"))

# wb.save('example.xls')

# from xlrd import open_workbook
# import xlwt
# from xlutils.copy import copy
#
# rb = open_workbook('example.xls',formatting_info=True)
# # rs = rb.sheet_by_index(0)
# wb = copy(rb)
#
# #wb.encoding='utf-8'
# ws = wb.get_sheet(0)
# ws.write(0,1,u'测试三')
# wb.save('example.xls')

import re
m = re.search(r'.*/(\d+)\.html','http://news.bingodu.com/2015/06/16/nh/1049062.html')
print type(int(m.group(1)))