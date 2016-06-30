#!/usr/bin/env python
# coding: utf-8

from random import choice
import string
import json
import os
import os.path
import paramiko
import sys
import hashlib

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
    def md5(content):
        md5 = hashlib.md5()
        md5.update(content)
        return md5.hexdigest()
    def __eq__(self, other):
        pass
    def __cmp__(self, other):
        pass

class User:
    def __init__(self,username=None,uid=None,pwd=None,homedir=None,key=None,pubkey=None,dash_key=None,
                 dash_pubkey=None,dash_keypassphrase=None,groups=None,shell="/bin/bash",email=None):
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
    def addGroup(self,group):
        self.groups.append(group)
        return self
    def getGroups(self):
        return self.groups
    def convert(self):
        dic = self.__dict__.copy()
        dic["groups"] = [ group.convert() for group in self.groups ] if self.groups else []
        dic["__cls__"] = str(self.__class__)
        return dic

class Host:
    def __init__(self,hostname=None,ip=None):
        self.hostname = hostname
        self.ip = ip
    def convert(self):
        dic = self.__dict__.copy()
        dic["__cls__"] = str(self.__class__)
        return dic

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

class UserManager:
    def __init__(self,*args):
        self.dbfile = "/root/.db/usersinfo.db"
        self.syncfile = "/root/.scripts/sync.json"
        self.dbusersinfo = JSONUtils.JSON2CustomObj(self.dbfile)
        self.sshcp = SSHConnectPool(username="ubuntu",key="/root/.ssh/gizwits_m2m.pem")
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
                out = self.sshcp.local("sudo groupadd -g "+gid+" "+groupname+" || /bin/true")
                return out
        else:
            if self.sshcp.remote(host,"grep -c '^"+groupname+":' /etc/group || /bin/true") == "0":
                out = self.sshcp.remote(host,"sudo groupadd -g "+gid+" "+groupname+" || /bin/true")
                return out
    def createUser(self,username,uid,groupnames,shell="/bin/bash",host=None):
        if not host:
            if self.sshcp.local("grep -c '^"+username+":' /etc/passwd || /bin/true") == "0":
                out = self.sshcp.local("sudo useradd -g "+groupnames[0] +" -G "+",".join(groupnames)+
                    " -u " +uid + " -m -s " + shell + " " + username + "|| /bin/true")
                return out
        else:
            if self.sshcp.remote(host,"grep -c '^"+username+":' /etc/passwd || /bin/true") == "0":
                out = self.sshcp.remote(host,"sudo useradd -g "+groupnames[0] +" -G "+",".join(groupnames)+
                    " -u " +uid + " -m -s " + shell + " " + username + "|| /bin/true")
                return out
    def generateRSA(self,username,key,dash_keypassphrase,dash_pubkey,dash_key,homedir):
        self.sshcp.local("sudo su " + username +" -c \"ssh-keygen -q -t rsa -f "+ key +" -N ''\"")
        self.sshcp.local("sudo su " + username +" -c \"ssh-keygen -q -t rsa -f "+ dash_key +" -N '"+dash_keypassphrase+"'\"")
        self.sshcp.local("sudo su "+username+" -c 'mkdir -p ~/.ssh; chmod 700 ~/.ssh; "
                                "touch ~/.ssh/authorized_keys; chmod 600 ~/.ssh/authorized_keys'")
        dashpubkeystr = self.sshcp.local("sudo cat "+dash_pubkey)
        self.sshcp.local("sudo bash -c 'echo "+dashpubkeystr+" >"+os.path.join(homedir,".ssh/authorized_keys")+"'")
    def addAuthorizedKey(self,pubkey,username,homedir,host):
        pubkeystr = self.sshcp.local("sudo cat "+pubkey)
        self.sshcp.remote(host,"sudo su "+username+" -c 'mkdir -p ~/.ssh; chmod 700 ~/.ssh; "
                                "touch ~/.ssh/authorized_keys; chmod 600 ~/.ssh/authorized_keys'")
        self.sshcp.remote(host,"sudo bash -c 'echo "+pubkeystr+" >"+os.path.join(homedir,".ssh/authorized_keys")+"'")
    def generateSSHConfigFile(self,users):
        for user in users:
            self.__fixuserattr(user)
            ipset=set()
            for group in user.getGroups():
                if not group.getHosts(): continue
                for host in group.getHosts():
                    ipset.add((host.ip,host.hostname))
            for iphost in ipset:
                self.sshcp.local("sudo bash -c 'cat >> "+os.path.join(user.homedir,".ssh/config")+"<<EOF"+"\n"
                        "Host "+iphost[1]+"\n"
                        " IdentityFile "+user.key+"\n"
                        " Port 22\n"
                        " HostName "+iphost[0]+"\n"
                        " User "+user.username+"\n"
                        "EOF\n'")
    # def createSudo(self,host):
    #     """
    #     %ops    ALL=(ALL)       NOPASSWD: ALL
    #     """
    #     self.sshcp.remote(host,"sudo bash -c 'cat \'%ops    ALL=(ALL)       NOPASSWD: ALL\'>>/etc/sudoers'")

    def sync(self):
        f_users = JSONUtils.JSON2CustomObj(self.syncfile)
        hostdic = {}
        for f_user in f_users:
            userdic = {}
            grouplist = userdic.setdefault(f_user.username,[])
            ipset=set()
            if self.checkUserExist(f_user.username):
                pass
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
                #建立创建远程用户和组所需的数据结构
                """
                hostdic = {
                ip1:[
                    {username1: [(gid1,gname),(gid2,gname),pubkey,homedir]}.
                    {username2: [(gid1,gname),(gid2,gname),pubkey,homedir]},
                   ]
                ip2:[
                    {username3: [(gid1,gname),(gid2,gname),pubkey,homedir]}.
                    {username4: [(gid1,gname),(gid2,gname),pubkey,homedir]},
                   ]
                }
                """
                for f_group in f_user.getGroups():
                    grouplist.append((f_group.gid,f_group.groupname))
                    if not f_group.getHosts(): continue
                    for host in f_group.getHosts():
                        ipset.add(host.ip)
                        hostdic.setdefault(host.ip,[])
                grouplist.append(f_user.pubkey)
                grouplist.append(f_user.homedir)
            for ip in ipset:
                hostdic[ip].append(userdic)

        for ip,ul in hostdic.items():
            if not ul: continue
            for u in ul:
                for username,gl in u.items():
                    groups = []
                    if not gl[:-2]: continue
                    for g in gl[:-2]:
                        #创建远程组
                        self.createGroup(g[1],g[0],host=ip)
                        groups.append(g[1])
                    #创建远程用户
                    self.createUser(username,groups[1],groups,host=ip)
                    self.sshcp.remote(ip,"sudo usermod -a -G sudo "+username)
                    self.addAuthorizedKey(gl[-2],username,gl[-1],ip)
            # self.createSudo(ip)

        #更新usersinfo.db
        for f_user in f_users:
            if self.dbusersinfo is None:
                self.dbusersinfo = {}
            self.dbusersinfo[f_user.username] = f_user
        self.__write2db(self.dbusersinfo)
        #更新dash用户的ssh配置文件
        self.generateSSHConfigFile(f_users)

if __name__ == "__main__":
    if len(sys.argv) == 1:
        UserManager("getuserinfo")
    else:
        UserManager(*sys.argv[1:])