#!/usr/bin/env python
# coding: utf-8

from random import choice
import string
import json
import os
import os.path
from fabric.api import *

class Group:
    def __init__(self, name, gid):
        self.name = name
        self.gid = gid
        self.hosts = []
        self.users = []
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
    def __str__(self):
        return "{0}({1})".format(self.name,self.gid)
    def __repr__(self):
        return "{0}({1})".format(self.name,self.gid)

class User:
    def __init__(self,username,uid,pwd=None):
        self.username = username
        self.uid = uid
        self.pwd = pwd
        self.homedir = "/home/" + self.username
        self.key = self.homedir + "/.ssh/id_rsa"
        self.pubkey = self.homedir +"/.ssh/id_rsa.pub"
        self.dash_key = self.homedir + "/.ssh/"+self.username+"_dash.key"
        self.dash_pubkey = self.homedir + "/.ssh/"+self.username+"_dash.key.pub"
        self.dash_keypassphrase = "".join([ choice(string.ascii_letters+string.digits+"!@#$%^&") for len in range(16) ])
        self.groups = [Group(self.username,self.uid),]
        self.shell = "/bin/bash"
    def addGroup(self,group):
        self.groups.append(group)
        return self
    def getGroups(self):
        return self.groups

class Host:
    def __init__(self,name,ip):
        self.name = name
        self.ip = ip
    def __str__(self):
        return "{0}({1})".format(self.name,self.ip)
    def __repr__(self):
        return "{0}({1})".format(self.name,self.ip)

# env.hosts = [
#                 "54.223.107.123",
#                 "54.223.112.103",
#                 "54.223.60.184",
#                 "54.223.62.193",
#                 "54.223.88.108",
#                 "54.223.105.134",
#                 "54.223.84.233",
#                 "54.223.93.73",
#                 "54.223.84.72",
#                 "54.223.81.208",
#                 "54.223.115.92",
#                 "54.223.113.124",
#                 "54.223.89.22",
#                 "54.223.101.16",
#                 "54.223.76.62",
#                 "54.223.112.255",
#                 "54.223.86.78"
#               ]

# effective_groups = [
#     Group("ops","2001")
#         .addUsers([
#             User("user1","1005"),
#         ])
#         .addHosts([
#             Host("mongo2","192.168.10.32"),
#         ]),
#     Group("dev","2002")
#         .addUsers([
#             User("user2","1006"),
#         ])
#         .addHosts([
#             Host("mongo2","192.168.10.33"),
#         ]),
# ]

def jsondump(obj,filename):
    with open(filename,'w') as f:
        json.dump(obj,f,indent=1)

def jsonload(filename):
    if os.path.isfile(filename):
        with open(filename,'r') as f:
            return json.load(f)
    return None

def generateGroupObjList(jsonfile):
    groups_list = jsonload(jsonfile)
    if not groups_list:
        print("Error: check the ./add.json file")
        exit()
    effective_groups = []
    for group in groups_list:
        group_obj = Group(group["groupname"],group["gid"])
        host_obj_list = []
        user_obj_list = []
        for user in group["users"]:
            user_obj_list.append(User(user["username"],user["uid"]))
        for host in group["hosts"]:
            host_obj_list .append(Host(host["hostname"],host["ip"]))
        group_obj.addHosts(host_obj_list).addUsers(user_obj_list)
        effective_groups.append(group_obj)
    return effective_groups

#initial fabric's environment
#env.roledefs = {'httpd': ['192.168.10.31', '192.168.10.32'], 'mysql': ['192.168.10.33',]}
usersinfofile = os.path.expanduser("~/.ssh/usersinfo.json")
effective_groups = generateGroupObjList("add.json")
rolesmap = {"localserver":[]}
for e_group in effective_groups:
    rolesmap[e_group.name] = [ host.ip for host in e_group.hosts ]
env.roledefs = rolesmap
env.user = "vagrant"
env.password = "vagrant"

def createLocalUser(users):
    for user in users:
        for group in user.getGroups():
            if os.popen("grep -c '^"+group.name+":' /etc/group").read().strip() == "0":
                os.popen("sudo groupadd -g " + group.gid + " " + group.name)
                print("[localhost]: create group {0}, gid {1} Done.".format(group.name,group.gid))
        if os.popen("grep -c '^"+ user.username + ":' /etc/passwd").read().strip() != "0": continue
        os.popen("sudo useradd -g "+user.getGroups()[0].gid+" -G "+
                ",".join([ group.gid for group in user.getGroups()[1:]])+
                " -u " +user.uid + " -m -s " + user.shell + " " + user.username
              )
        print("[localhost]: create user {0}, uid {1} Done.".format(user.username,user.uid))
        os.popen("sudo su " + user.username +" -c \"ssh-keygen -q -t rsa -f "+ user.key +" -N ''\"")
        os.popen("sudo su " + user.username +" -c \"ssh-keygen -q -t rsa -f "+ user.dash_key +" -N '"+user.dash_keypassphrase+"'\"")
        """
        run("sudo su "+user.username+" -c 'mkdir -p ~/.ssh; chmod 700 ~/.ssh; "
                                "touch ~/.ssh/authorized_keys; chmod 600 ~/.ssh/authorized_keys'")
        run("sudo bash -c 'echo "+pubkeystr+" >>"+os.path.join(user.homedir,".ssh/authorized_keys")+"'")
        """
        os.popen("sudo su "+user.username+" -c 'mkdir -p ~/.ssh; chmod 700 ~/.ssh; "
                                "touch ~/.ssh/authorized_keys; chmod 600 ~/.ssh/authorized_keys'")
        dashpubkeystr = os.popen("sudo cat "+user.dash_pubkey).read().strip()
        os.popen("sudo bash -c 'echo "+dashpubkeystr+" >"+os.path.join(user.homedir,".ssh/authorized_keys")+"'")
        print("[localhost]: user {0}, ssh-keygen done.".format(user.username))

def generateUserInfo(users):
    usersinfo = jsonload(usersinfofile)
    if not usersinfo: usersinfo = []
    for user in users:
        userinfo = {}
        userinfo["username"] = user.username
        userinfo["uid"] = user.uid
        userinfo["homedir"] = user.homedir
        userinfo["key"] = user.key
        userinfo["pubkey"] = user.pubkey
        userinfo["dash_key"] = user.dash_key
        userinfo["dash_pubkey"] =user.dash_pubkey
        userinfo["dash_keypassphrase"] = user.dash_keypassphrase
        userinfo["shell"] = user.shell
        userinfo["groups"] = [ {"groupname": group.name, "gid": group.gid } for group in user.getGroups()]
        userinfo["hosts"] = [ {"hostname":host.name, "ip": host.ip}
                              for group in user.getGroups()[1:] for host in group.getHosts() ]
        usersinfo.append(userinfo)
    jsondump(usersinfo,usersinfofile)

def generateSSHConfigFile(users):
    for user in users:
        for group in user.getGroups()[1:]:
            for host in group.getHosts():
                local("sudo bash -c 'cat >> "+os.path.join(user.homedir,".ssh/config")+"<<EOF"+"\n"
                        "Host "+host.name+"\n"
                        " IdentityFile "+user.key+"\n"
                        " Port 22\n"
                        " HostName "+host.ip+"\n"
                        " User "+user.username+"\n"
                        "EOF\n'")

def createRemoteUser(users):
    for user in users:
        for group in user.getGroups():
            if run("grep -c '^"+group.name+":' /etc/group || /bin/true",warn_only=True).strip() == "0":
                run("sudo groupadd -g " + group.gid + " " + group.name)
        if run("grep -c '^"+user.username+":' /etc/passwd || /bin/true", warn_only=True).strip() != "0": continue
        run("sudo useradd -g "+user.getGroups()[0].gid+" -G "+
                ",".join([ group.gid for group in user.getGroups()[1:]])+
                " -u " +user.uid + " -m -s " + user.shell + " " + user.username)
        pubkeystr = local("sudo cat "+user.pubkey,capture=True).stdout.strip()
        run("sudo su "+user.username+" -c 'mkdir -p ~/.ssh; chmod 700 ~/.ssh; "
                                "touch ~/.ssh/authorized_keys; chmod 600 ~/.ssh/authorized_keys'")
        run("sudo bash -c 'echo "+pubkeystr+" >"+os.path.join(user.homedir,".ssh/authorized_keys")+"'")


@roles("localserver")
def roleTask1():
    users = set([ user for e_group in effective_groups for user in e_group.users ])
    createLocalUser(users)
    generateUserInfo(users)
    generateSSHConfigFile(users)


@roles("ops")
def roleTask2():
    users = [ user for e_group in effective_groups if e_group.name == "ops" for user in e_group.users ]
    createRemoteUser(users)

@roles("dev")
def roleTask3():
    users = [ user for e_group in effective_groups if e_group.name == "dev" for user in e_group.users ]
    createRemoteUser(users)

@task
def useradd():
    execute(roleTask1)
    # execute(roleTask2)
    # execute(roleTask3)

@task
def usermod(username,):
    pass

@task
def userdel():
    pass

@task
def groupadd():
    pass

@task
def groupdel():
    pass

@task
def groupmod():
    pass















