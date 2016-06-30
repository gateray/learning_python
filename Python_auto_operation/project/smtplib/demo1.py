#!/usr/bin/env python
# coding: utf-8

from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText

# python 2.3.*: email.Utils email.Encoders
from email.utils import COMMASPACE,formatdate
from email import encoders

import os

#server['name'], server['user'], server['passwd']
def send_mail(server, fro, to, subject, text, files=[]):
    assert type(server) == dict
    assert type(to) == list
    assert type(files) == list

    msg = MIMEMultipart()
    msg['From'] = fro
    msg['Subject'] = subject
    msg['To'] = COMMASPACE.join(to[:-1]) #COMMASPACE==', '
    msg['CC'] = "1492604006@qq.com"
    msg['Date'] = formatdate(localtime=True)
    msg.attach(MIMEText(text))

    for file in files:
        part = MIMEBase('application', 'octet-stream') #'octet-stream': binary data
        part.set_payload(open(file, 'rb').read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(file))
        msg.attach(part)

    import smtplib
    smtp = smtplib.SMTP(server['name'])
    smtp.login(server['user'], server['passwd'])
    smtp.sendmail(fro, to, msg.as_string())
    smtp.close()


if __name__ == "__main__":
    server = {
        "name" : "smtp.163.com",
        "user" : "zabbixonlytest",
        "passwd" : "hdqupxpgxnpdmsme",
    }
    fro = "zabbixonlytest@163.com"
    to = [
        "437925289@qq.com",
    ]
    subject="Python Sendmail Test2"
    text = "send text with attach\n"
    files = [
        os.path.expanduser("~/桌面/1.jpg"),
    ]
    to.append("1492604006@qq.com")
    send_mail(server, fro, to,subject,text,files)