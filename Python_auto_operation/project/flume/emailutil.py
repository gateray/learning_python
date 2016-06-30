#!/usr/bin/env python
# coding: utf-8

from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from os.path import basename,expanduser

class EMailUtil:
    def __init__(self,subject,from_addr,to_list,cc_list=None):
        """
        subject(str): 邮件主题
        from_user(str): 发送人email
        to_list(list): 收件人列表
        cc_list(list): 抄送列表
        """
        self.subject = subject
        self.from_addr = from_addr
        self.to_list = to_list
        self.cc_list = cc_list
        self._msg = MIMEMultipart("alternative")
        self.defaultsign = '''
        <div>
          <sign signid="0">
            <div style="color:#909090;font-family:Arial Narrow;font-size:12px">
              <br>
              <br>
              <br>
              <br>
              ------------------
            </div>
            <div style="font-size:14px;font-family:Verdana;color:#000;">
              <div>
                <p style="color: rgb(34, 34, 34); font-family: arial, sans-serif; font-size: 13px; line-height: normal; margin: 0cm 0cm 0pt;">
                  <i>
                    <span lang="EN-US" style="font-family: Arial, sans-serif; color: rgb(10, 10, 10); font-size: 10pt;">
                      Best Regards
                    </span>
                  </i>
                  <font face="宋体">
                    <i>
                      <span style="color: rgb(10, 10, 10); font-size: 10pt;">
                        ，
                      </span>
                    </i>
                  </font>
                </p>
                <p style="color: rgb(34, 34, 34); font-family: arial, sans-serif; font-size: 13px; line-height: normal; margin: 0cm 0cm 0pt;">
                  <font face="宋体">
                    <i>
                      <span style="color: rgb(10, 10, 10); font-size: 10pt;">
                      </span>
                    </i>
                    <i>
                      <span lang="EN-US" style="font-family: Arial, sans-serif; color: rgb(10, 10, 10); font-size: 10pt;">
                      </span>
                    </i>
                  </font>
                  &nbsp;
                </p>
                <p style="color: rgb(34, 34, 34); font-family: arial, sans-serif; font-size: 12.727272033691406px; line-height: normal; margin: 0cm 0cm 0pt;">
                  <span lang="EN-US" style="color: rgb(10, 10, 10);">
                    <font face="宋体" style="font-size: 17px;">
                      周冠伟 Guyray Zhou
                    </font>
                    <font style="font-family: Arial, sans-serif;">
                      &nbsp;
                    </font>
                  </span>
                  <i>
                    <span lang="EN-US" style="font-family: Arial, sans-serif; color: rgb(10, 10, 10); font-size: 10pt;">
                      <br>
                    </span>
                  </i>
                  <br>
                </p>
                <p style="margin: 0cm 0cm 0pt;">
                  <font color="#0a0a0a" face="Arial, sans-serif">
                    <span style="font-size: 13.3333330154419px; line-height: normal;">
                      Release Manager
                    </span>
                  </font>
                </p>
                <p style="margin: 0cm 0cm 0pt;">
                  <span style="font-size: 13.3333330154419px; line-height: normal; color: rgb(10, 10, 10); font-family: Arial, sans-serif;">
                    T: 020-37684150
                  </span>
                </p>
                <p style="margin: 0cm 0cm 0pt;">
                  <span style="font-size: 13.3333330154419px; line-height: normal; color: rgb(10, 10, 10); font-family: Arial, sans-serif;">
                    M: 13265083405
                  </span>
                </p>
                <p style="margin: 0cm 0cm 0pt;">
                  <span style="font-size: 13.3333330154419px; line-height: normal; color: rgb(10, 10, 10); font-family: Arial, sans-serif;">
                    机智云 只为智能硬件而生
                  </span>
                </p>
                <p style="margin: 0cm 0cm 0pt;">
                  <span style="line-height: 1.5;">
                    <a href="http://gizwits.com/" target="_blank" style="outline: none; color: rgb(42, 88, 111); font-family: Verdana, sans-serif; font-size: 13.3333px; line-height: 22.4px;">
                      Gizwits
                    </a>
                    <span style="font-family: Verdana, sans-serif; font-size: 13.3333px; line-height: 22.4px;">
                      &nbsp;
                    </span>
                    <span lang="EN-US" style="font-size: 10pt; line-height: 22.4px; font-family: Verdana, sans-serif;">
                      Smart Cloud
                    </span>
                    <span style="font-family: Verdana, sans-serif; font-size: 13.3333px; line-height: 22.4px;">
                      for Smart Products
                    </span>
                  </span>
                </p>
                <p style="margin: 0cm 0cm 0pt;">
                  <b style="font-size: 13.3333330154419px; line-height: normal; color: rgb(10, 10, 10); font-family: Arial, sans-serif;">
                    连接｜ 增值｜开放 ｜中立｜安全｜自有｜自由｜生态
                  </b>
                </p>
                <p style="margin: 0cm 0cm 0pt;">
                  <b style="font-size: 13.3333330154419px; line-height: normal; color: rgb(10, 10, 10); font-family: Arial, sans-serif;">
                    www.gizwits.com
                  </b>
                </p>
                <p style="margin: 0cm 0cm 0pt;">
                  <img src="http://exmail.qq.com/cgi-bin/viewfile?type=signature&amp;picid=ZX0331-GKTfgNfaT_3n63AlL_xGM53&amp;uin=2612156348"
                  width="150" height="150" style="line-height: 1.5;">
                </p>
              </div>
            </div>
          </sign>
        </div>
        '''
    def addAttach(self,attach_list):
        """
        添加邮件附件
        attach_list(list):附件文件名列表
        """
        for file in attach_list:
            file = expanduser(file)
            part = MIMEBase('application', 'octet-stream')
            with open(file,'rb') as fp:
                part.set_payload(fp.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', 'attachment', filename=basename(expanduser(file)))
            self._msg.attach(part)

    def addMessage(self,content,type="plain"):
        """
        用于添加简单邮件内容,仅支持text和html内容
        """
        part = MIMEText(content,_subtype=type,_charset="utf-8")
        self._msg.attach(part)

    def addMessageFromFile(self,filename,type="plain",cid=""):
        """
        添加邮件内容
        filename(str): 邮件内容,从filename指定的文件中获取
        type(str):
            "text": 文本
            "html": html
            "image": 图片
            "cid": 基于html格式展示图片时,<img src="cid:xxx">需要使用cid
        """
        filename = expanduser(filename)
        if type in ("plain","html"):
            fp = open(filename)
            part = MIMEText(fp.read(),_subtype=type,_charset="utf-8")
            fp.close()
        elif type == "image":
            fp = open(filename,'rb')
            part = MIMEImage(fp.read())
            part.add_header("Content-ID", cid)
            fp.close()
        else:
            return
        self._msg.attach(part)

    def addSign(self,text,image=None):
        """
        添加邮件签名
        text(str): 签名的文本部分
        image(str): 图片文件名,签名的图片部分
        """
        self.addMessage(text)
        if image:
            self.addMessageFromFile(image,type="image")

    def sendmail(self,smtpserver,username=None,password=None,port=25):
        import smtplib
        smtp = smtplib.SMTP()
        smtp.connect(smtpserver,port)
        # smtp.starttls()
        if username and password: smtp.login(username,password)
        self._msg["Subject"] = self.subject
        self._msg["From"] = self.from_addr
        if isinstance(self.to_list,list):
            self._msg["To"] = ", ".join(self.to_list)
        elif isinstance(self.to_list,str):
            self.to_list = [ self.to_list ]
            self._msg["To"] = ", ".join(self.to_list)
        else:
            return
        if isinstance(self.cc_list,list):
            self._msg["CC"] = ", ".join(self.cc_list)
        elif isinstance(self.cc_list,str):
            self.cc_list = [ self.cc_list ]
            self._msg["CC"] = ", ".join(self.cc_list)
        else:
            self.cc_list = []
        # smtp.send(self._msg.as_string())
        smtp.sendmail(self.from_addr,self.to_list+self.cc_list,self._msg.as_string())
        smtp.quit()

