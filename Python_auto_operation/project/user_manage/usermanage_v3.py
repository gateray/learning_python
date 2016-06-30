#!/usr/bin/env python
# coding: utf-8

from random import choice
import string
import json
import os
import os.path
import paramiko
import sys

class Group:
    def __init__(self, groupname=None, gid=None, hosts=None,users=None):
        self.groupname = groupname
        self.gid = gid
        self.hosts = hosts if hosts else []
        self.users = users if users else []
    def addHost(self,host):
        self.hosts.append(host)
        return self
    def addHosts(self,hosts):
        for host in hosts:
            self.addHost(host)
        return self
    def removeHost(self,host):
        self.hosts.remove(host)
    def addUser(self,user):
        self.users.append(user)
        user.addGroup(self)
        return self
    def addUsers(self,users):
        for user in users:
            self.addUser(user)
        return self
    def getHosts(self):
        return self.hosts
    def getUsers(self):
        return self.users
    def convert(self):
        dic = self.__dict__.copy()
        dic["hosts"] = [ host.convert() for host in self.hosts ] if self.hosts else []
        dic["users"] = [ user.convert() for user in self.users ] if self.users else []
        dic["__cls__"] = str(self.__class__)
        return dic
    def __eq__(self, other):
        if isinstance(other,Group):
            return self.gid.__eq__(other.gid) or self.groupname.__eq__(other.groupname)
        else:
            return False
    def __hash__(self):
        if self.gid:
            return hash(self.gid)
        if self.groupname:
            return hash(self.groupname)
        return super.__hash__(self)
    def hasHostChanged(self,objlist):
        def diff(myset,yourset):
            reduce = myset.difference((myset.intersection(yourset)))
            increase = yourset.difference((myset.intersection(yourset)))
            return (increase,reduce)
        if isinstance(objlist,list):
            yourhosts = set()
            for obj in objlist:
                if isinstance(obj,Host):
                    yourhosts.add(obj)
            myhosts = set(self.getHosts()) if self.getHosts() else set()
            dif = diff(myhosts,yourhosts)
            if len(dif[0]) == 0 and len(dif[1]) == 0:
                return False
            else:
                return dif
        else:
            return False

class User:
    def __init__(self,username=None,uid=None,pwd=None,homedir=None,key=None,pubkey=None,dash_key=None,
                 dash_pubkey=None,dash_keypassphrase=None,groups=None,shell="/bin/bash",email=""):
        self.username = username
        self.uid = uid
        self.pwd = pwd
        self.homedir = homedir
        self.key = key
        self.pubkey = pubkey
        self.dash_key = dash_key
        self.dash_pubkey = dash_pubkey
        self.dash_keypassphrase = dash_keypassphrase
        self.groups = groups if groups else []
        self.shell = shell
        self.email = email
        self.ischange = False
    def addGroup(self,group):
        self.groups.append(group)
        return self
    def getGroups(self):
        return self.groups
    def removeGroup(self,group):
        self.groups.remove(group)
    def convert(self):
        dic = self.__dict__.copy()
        dic["groups"] = [ group.convert() for group in self.groups ] if self.groups else []
        dic["__cls__"] = str(self.__class__)
        return dic
    def __eq__(self, other):
        if isinstance(other,User):
            return self.uid.__eq__(other.uid) or self.username.__eq__(other.username)
        else:
            return False
    def __hash__(self):
        if self.uid:
            return hash(self.uid)
        if self.username:
            return hash(self.username)
        return super.__hash__(self)
    def hasGroupChanged(self,objlist):
        def diff(myset,yourset):
            reduce = myset.difference((myset.intersection(yourset)))
            increase = yourset.difference((myset.intersection(yourset)))
            return (increase,reduce)
        if isinstance(objlist,list):
            yourgroups = set()
            mygroups = set(self.getGroups())
            for obj in objlist:
                if isinstance(obj,Group):
                    yourgroups.add(obj)
            dif = diff(mygroups,yourgroups)
            if len(dif[0]) == 0 and len(dif[1]) == 0:
                return False
            else:
                return dif
        else:
            return False

class Host:
    def __init__(self,hostname=None,ip=None):
        self.hostname = hostname
        self.ip = ip
    def convert(self):
        dic = self.__dict__.copy()
        dic["__cls__"] = str(self.__class__)
        return dic
    def __eq__(self, other):
        if isinstance(other,Host):
            return self.ip.__eq__(other.ip) or self.hostname.__eq__(other.hostname)
        else:
            return False
    def __hash__(self):
        if self.ip:
            return hash(self.ip)
        if self.hostname:
            return hash(self.hostname)
        return super.__hash__(self)

class JSONUtils:
    class MyJSONEncoder(json.JSONEncoder):
        def default(self, o):
            if isinstance(o,(User,Group,Host)):
                return o.convert()
            return json.JSONEncoder.default(self, o)
    @staticmethod
    def jsondump(obj,filename):
        with open(filename,'w') as f:
            json.dump(obj,f,indent=2,cls=JSONUtils.MyJSONEncoder)
    @staticmethod
    def jsonload(filename):
        if os.path.isfile(filename):
            with open(filename,'r') as f:
                return json.load(f)
        return None
    @staticmethod
    def customObj2Dict(obj):
        return obj.convert()
    @staticmethod
    def dict2Obj(dic,obj):
        for k,v in dic.items():
            if hasattr(obj,k):setattr(obj,k,v)
        return obj
    @staticmethod
    def JSON2CustomObj(jsonfile):
        if not os.path.isfile(jsonfile):
            return None
        def hook(dic):
            flag = False
            if type(dic) not in [list,dict]:return dic
            if isinstance(dic,dict) and '__cls__' in dic:
                for k,v in dic.items():
                    dic[k] = hook(v)
                simplename = dic["__cls__"].split(".")[-1]
                return JSONUtils.dict2Obj(dic,globals()[simplename]())
            elif isinstance(dic,dict):#dict
                for k,v in dic.items():
                    dic[k] = hook(v)
                    return dic
            else:#list
                for i,elm in enumerate(dic):
                    dic[i] = hook(elm)
                    return dic
        with open(jsonfile) as f:
            return json.load(f,object_hook=hook)
    @staticmethod
    def printJSONFile(jsonfile):
        if not os.path.isfile(jsonfile):
            return None
        with open(jsonfile) as f:
            for line in f:
                print(line),

class SSHConnectPool:
    def __init__(self,username="root",pwd=None,key=None):
        self.username = username
        self.pwd = pwd
        self.key = key
        self.sshpool = {}
    def newConnect(self,host):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        if self.key:
            keyObj = paramiko.RSAKey.from_private_key_file(self.key)
            ssh.connect(host,username=self.username,pkey=keyObj,timeout=900)
        else:
            ssh.connect(host,username=self.username,password=self.pwd,timeout=900)
        return ssh
    def getConnection(self,host):
        if not self.sshpool.has_key(host):
            self.sshpool[host] = self.newConnect(host)
        return self.sshpool[host]
    def releaseConnection(self,*hosts):
        if not hosts:
            for ssh in self.sshpool.values():
                ssh.close()
        else:
            for host in hosts:
                self.sshpool[host].close()
    def local(self,cmd):
        std = os.popen(cmd)
        out = std.read().strip()
        print("[localhost]:\n"
              "  execute: "+cmd+"\n"
              "  out: "+out)
        std.close()
        return out
    def remote(self,host,cmd):
        ssh = self.getConnection(host)
        stdin,stdout,stderr = ssh.exec_command(cmd)
        out,err = stdout.read().strip(),stderr.read().strip()
        if out:
            print("["+host+"]:\n"
                  "  execute: "+cmd+"\n"
                  "  out: "+out)
            return out
        if err:
            print("  warn: "+err)

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
        self.defaultsign = u'''
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
        self.addMessage(text,type="html")
        if image:
            self.addMessageFromFile(image,type="image")

    def sendmail(self,smtpserver,username,password,port=25):
        import smtplib
        smtp = smtplib.SMTP()
        smtp.connect(smtpserver,port)
        # smtp.starttls()
        smtp.login(username,password)
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

class UserManager:
    def __init__(self,*args):
        self.dbfile = "usersinfo.db"
        self.syncfile = "sync.json"
        self.dbusersinfo = JSONUtils.JSON2CustomObj(self.dbfile)
        self.sshcp = SSHConnectPool(username="vagrant",pwd="vagrant")
        cmd = args[0]
        getattr(self,cmd)(*args[1:])
    def __write2db(self,dbusersinfo):
        JSONUtils.jsondump(dbusersinfo,self.dbfile)
    def __fixuserattr(self,user):
        user.homedir = "/home/" + user.username if not user.homedir else user.homedir
        user.key = user.homedir + "/.ssh/id_rsa" if not user.key else user.key
        user.pubkey = user.homedir +"/.ssh/id_rsa.pub" if not user.pubkey else user.pubkey
        user.dash_key = user.homedir + "/.ssh/"+user.username+"_dash.key" \
            if not user.dash_key else user.dash_key
        user.dash_pubkey = user.homedir + "/.ssh/"+user.username+"_dash.key.pub" \
            if not user.dash_pubkey else user.dash_pubkey
        user.dash_keypassphrase = user.dash_keypassphrase if user.dash_keypassphrase \
            else "".join([ choice(string.ascii_letters+string.digits+"!@#$%^&") for len in range(16) ])
        user.email = user.username+"@gizwits.com" if not user.email else user.email
    def checkUserExist(self,username):
        if self.dbusersinfo:
            return self.dbusersinfo.has_key(username)
        return False
    def getuserinfo(self,*usernames):
        if not self.dbusersinfo: return
        if len(usernames) == 0:
            users = [v for v in self.dbusersinfo.values()]
        else:
            users = [ self.dbusersinfo[k] for k in usernames if self.dbusersinfo.has_key(k)]
        JSONUtils.jsondump(users,self.syncfile)
        JSONUtils.printJSONFile(self.syncfile)
    def createGroup(self,groupname,gid,host=None):
        if not host:
            if self.sshcp.local("grep -c '^"+groupname+":' /etc/group || /bin/true") == "0":
                return self.sshcp.local("sudo groupadd -g "+gid+" "+groupname+" && echo 0 || echo 1")
        else:
            if self.sshcp.remote(host,"grep -c '^"+groupname+":' /etc/group || /bin/true") == "0":
                out = self.sshcp.remote(host,"sudo groupadd -g "+gid+" "+groupname+" && echo 0 || echo 1")
                return out
    def createUser(self,username,uid,groupnames,shell="/bin/bash",host=None):
        if not host:
            if self.sshcp.local("grep -c '^"+username+":' /etc/passwd || /bin/true") == "0":
                return self.sshcp.local("sudo useradd -g "+username +" -G "+",".join(groupnames)+
                    " -u " +uid + " -m -s " + shell + " " + username + " && echo 0 || echo 1")
        else:
            if self.sshcp.remote(host,"grep -c '^"+username+":' /etc/passwd || /bin/true") == "0":
                out = self.sshcp.remote(host,"sudo useradd -g "+username +" -G "+",".join(groupnames)+
                    " -u " +uid + " -m -s " + shell + " " + username + " && echo 0 || echo 1")
                return out
    def deleteUser(self,username,host=None):
        if not host:
            if self.sshcp.local("grep -c '^"+username+":' /etc/passwd || /bin/true") != "0":
                return self.sshcp.local("sudo userdel -r "+username +" && echo 0 || echo 1")
        else:
            if self.sshcp.remote(host,"grep -c '^"+username+":' /etc/passwd || /bin/true") != "0":
                out = self.sshcp.remote(host,"sudo userdel -r " + username + " && echo 0 || echo 1")
                return out
    def modifyUser(self,username,groups,host=None):
        if not host:
            if self.sshcp.local("grep -c '^"+username+":' /etc/passwd || /bin/true") != "0":
                return self.sshcp.local("sudo usermod -G "+",".join([ group.groupname for group in groups ])
                                        +" " + username +" && echo 0 || echo 1")
        else:
            if self.sshcp.remote(host,"grep -c '^"+username+":' /etc/passwd || /bin/true") != "0":
                out = self.sshcp.remote(host,"sudo usermod -G "+",".join([ group.groupname for group in groups ])
                                        +" " + username +" && echo 0 || echo 1")
                return out
    def generateRSA(self,username,key,dash_keypassphrase,dash_pubkey,dash_key,homedir):
        self.sshcp.local("sudo su " + username +" -c \"ssh-keygen -q -t rsa -f "+ key +" -N ''\"")
        self.sshcp.local("sudo su " + username +" -c \"ssh-keygen -q -t rsa -f "+ dash_key +" -N '"+
                         dash_keypassphrase+"'\"")
        self.sshcp.local("sudo su "+username+" -c 'mkdir -p ~/.ssh; chmod 700 ~/.ssh; "
                                "touch ~/.ssh/authorized_keys; chmod 600 ~/.ssh/authorized_keys'")
        self.addAuthorizedKey(dash_pubkey,username,homedir,host=None)
        # dashpubkeystr = self.sshcp.local("sudo cat "+dash_pubkey)
        # self.sshcp.local("sudo bash -c 'echo "+dashpubkeystr+" >"+os.path.join(homedir,".ssh/authorized_keys")+"'")
    def addAuthorizedKey(self,pubkey,username,homedir,host=None):
        pubkeystr = self.sshcp.local("sudo cat "+pubkey)
        if not host:
            self.sshcp.local("sudo bash -c 'echo "+pubkeystr+" >"+os.path.join(homedir,".ssh/authorized_keys")+"'")
        else:
            self.sshcp.remote(host,"sudo su "+username+" -c 'mkdir -p ~/.ssh; chmod 700 ~/.ssh; "
                                    "touch ~/.ssh/authorized_keys; chmod 600 ~/.ssh/authorized_keys'")
            self.sshcp.remote(host,"sudo bash -c 'echo "+pubkeystr+" >"+os.path.join(homedir,".ssh/authorized_keys")+"'")
    def generateSSHConfigFile(self,users):
        for user in users:
            self.__fixuserattr(user)
            hostset=set()
            for group in user.getGroups():
                if not group.getHosts(): continue
                for host in group.getHosts():
                    hostset.add((host))
            self.sshcp.local("sudo bash -c '>"+os.path.join(user.homedir,".ssh/config")+"'")
            for host in hostset:
                self.sshcp.local("sudo bash -c 'cat >> "+os.path.join(user.homedir,".ssh/config")+"<<EOF"+"\n"
                        "Host "+host.hostname+"\n"
                        " IdentityFile "+user.key+"\n"
                        " Port 22\n"
                        " HostName "+host.ip+"\n"
                        " User "+user.username+"\n"
                        "EOF\n'")
    def sync(self):
        def createUserAndGroup(f_user,hostset=None):
            groupset = set(f_user.getGroups())
            if not hostset:
                hostset = set()
                for f_group in groupset:
                    if not f_group.getHosts(): continue
                    for f_host in f_group.getHosts():
                        hostset.add(f_host)
            for host in hostset:
                flag = False
                for group in groupset:
                    if self.createGroup(groupname=group.groupname,gid=group.gid,host=host.ip) == "1":
                        group.removeHost(Host(ip=host.ip))
                        flag = True
                    if flag: break
                if flag: continue
                if self.createUser(f_user.username,f_user.uid,[group.groupname for group in groupset],shell=f_user.shell,host=host.ip) == "1":
                    group.removeHost(Host(ip=host.ip))
                    continue
                self.addAuthorizedKey(f_user.pubkey,f_user.username,f_user.homedir,host.ip)
        def removeUserAndGroup(f_user,myuser,hostset=None):
            if not hostset:
                hostset = set()
                mygroupset = set(myuser.getGroups())
                for mygroup in mygroupset:
                    if not mygroup.getHosts(): continue
                    for myhost in mygroup.getHosts():
                        hostset.add(myhost)
            for host in hostset:
                self.deleteUser(f_user.username,host=host.ip)
        f_users = JSONUtils.JSON2CustomObj(self.syncfile)
        if not f_users:
            print("check your sync.json file.")
            return
        for f_user in f_users:
            if self.checkUserExist(f_user.username):
                #检查用户所在组是否发生变化
                myuser = self.dbusersinfo[f_user.username]
                mygroups = myuser.getGroups()
                f_groups = f_user.getGroups()
                g_diff = myuser.hasGroupChanged(f_groups)
                if not f_groups: #当所有组都不存在时
                    #删除远程用户
                    removeUserAndGroup(f_user,myuser)
                    self.deleteUser(f_user.username)
                    continue
                if g_diff: #组有变
                    f_user.ischange = True
                    #修改本地用户和组:
                    self.modifyUser(f_user.username,f_user.getGroups())
                    #修改远程用户和组
                    for mygroup in mygroups:
                        if not mygroup.getHosts(): continue
                        for myhost in mygroup.getHosts():
                            self.modifyUser(f_user.username,f_user.getGroups(),myhost.ip)
                    for inc_group in g_diff[0]:
                        mygroups.append(Group(groupname=inc_group.groupname,gid=inc_group.gid))
                    for red_group in g_diff[1]:
                        f_groups.append(Group(groupname=red_group.groupname,gid=red_group.gid))
                #检查主机是否发生变化
                for mygroup in mygroups:
                    try:
                        if f_groups is None: break
                        index = f_groups.index(mygroup)
                    except ValueError,AttributeError:
                        continue
                    f_group = f_groups[index]
                    h_diff = mygroup.hasHostChanged(f_group.getHosts())
                    if not h_diff: #主机没变
                        continue
                    else: #主机有变
                        if not f_user.ischange: f_user.ischange = True
                        increase,reduce = h_diff
                        if len(increase) > 0:
                            for host in increase:
                                #新增主机上创建用户和组
                                createUserAndGroup(f_user,increase)
                        if len(reduce) > 0:
                            removeUserAndGroup(f_user,myuser,reduce)
            else:
                self.__fixuserattr(f_user)
                #创建本地组
                for f_group in f_user.getGroups():
                    self.createGroup(f_group.groupname,f_group.gid)
                #创建本地用户并加入组
                self.createUser(f_user.username,f_user.uid,[ group.groupname for group in f_user.getGroups()])
                #生成密钥文件
                self.generateRSA(f_user.username,f_user.key,f_user.dash_keypassphrase,f_user.dash_pubkey,
                                 f_user.dash_key,f_user.homedir)
                #创建远程用户和组
                createUserAndGroup(f_user)
                f_user.ischange = True
                #发送邮件
                eu = EMailUtil(u"AWS账号及登录方式","zabbixonlytest@163.com",[f_user.email,])
                eu.addMessage(u"<div><p>server远程访问方法: 先ssh到dash,再跳转到目标主机</p>"
                              u"<p>ssh到dash:</p>"
                              u"&nbsp;&nbsp;<span>username: "+f_user.username+u"</span><br/>"
                              u"&nbsp;&nbsp;<span>dashkey: 见附件</span><br/>"
                              u"&nbsp;&nbsp;<span>passphrase: "+f_user.dash_keypassphrase+u"</span><br/>"
                              u"&nbsp;&nbsp;<span>将dashkey的权限修改成600: chmod 600 /path/to/"+os.path.basename(f_user.dash_key)+"</span><br/>"
                              u"&nbsp;&nbsp;<span>登录命令: ssh -i /path/to/"+os.path.basename(f_user.dash_key)+" "
                                +f_user.username+u"@54.223.107.193 (按提示输入你的passphrase)</span><br/>"
                              u"<br/>"
                              u"<p>从dash跳转到目标主机:</p>"
                              u"&nbsp;&nbsp;<span>ssh 目标主机名称,如:ssh LQASite01</span><br/>"
                              u"&nbsp;&nbsp;<span>当前用户所有可登录的目标主机名称位于~/.ssh/config文件下,"
                              u"查看方法: cat ~/.ssh/config</span><br/>"
                              u"</div>"+eu.defaultsign,type="html")
                eu.addAttach([f_user.dash_key,])
                eu.sendmail("smtp.163.com","zabbixonlytest","hdqupxpgxnpdmsme")
        #更新usersinfo.db

        for f_user in f_users:
            if not f_user.ischange:
                f_users.remove(f_user)
                continue
            if self.dbusersinfo is None:
                self.dbusersinfo = {}
            f_user.ischange = False
            self.dbusersinfo[f_user.username] = f_user
        self.__write2db(self.dbusersinfo)
        #更新dash用户的ssh配置文件
        self.generateSSHConfigFile(f_users)
        print("Done.")

if __name__ == "__main__":
    if len(sys.argv) == 1:
        UserManager("getuserinfo")
    else:
        UserManager(*sys.argv[1:])