#!/usr/bin/env python
# coding: utf-8

import smtplib
from email.mime.text import MIMEText

sender = 'zabbixonlytest@163.com'
receiver = '437925289@qq.com'
subject = 'python email test'
smtpserver = 'smtp.163.com'
username = 'zabbixonlytest'
password = 'hdqupxpgxnpdmsme'

msg = MIMEText('<html><h1>你好</h1></html>','html','utf-8')

msg['Subject'] = subject

smtp = smtplib.SMTP()
smtp.connect(smtpserver)
smtp.login(username, password)
smtp.sendmail(sender, receiver, msg.as_string())
smtp.quit()
