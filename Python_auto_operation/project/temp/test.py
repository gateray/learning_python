#!/usr/bin/env python
# coding: utf-8

class Group:
    def __init__(self, groupname=None, gid=None, hosts=[],users=[]):
        self.groupname = groupname
        self.gid = gid
        self.hosts = hosts
        self.users = users
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
        dic["hosts"] = [ host.convert() for host in self.hosts ]
        dic["users"] = [ user.convert() for user in self.users ]
        dic["__cls__"] = str(self.__class__)
        return dic

class User:
    def __init__(self,username=None,uid=None,pwd=None,homedir=None,key=None,pubkey=None,dash_key=None,
                 dash_pubkey=None,dash_keypassphrase=None,groups=None,shell="/bin/bash"):
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
    def addGroup(self,group):
        self.groups.append(group)
        return self
    def getGroups(self):
        return self.groups
    def convert(self):
        dic = self.__dict__.copy()
        dic["groups"] = [ group.convert() for group in self.groups ]
        dic["__cls__"] = str(self.__class__)
        return dic

if __name__ == "__main__":
    user1 = User(username="user1",uid="2001")
    user1.addGroup(Group(groupname="user1",gid="2001"))
    # user1.addGroup(Group(groupname="ops",gid="3001"))
    print(user1.getGroups())
    # user2 = User(username="user2",uid="2002")
    user3 = User()
    # # user2.addGroup(Group(groupname="user2",gid="2002"))
    # # user2.addGroup(Group(groupname="dev",gid="3002"))
    # # JSONUtils.jsondump([user1,user2],'addlocaluser.json')
    # print(user2.getGroups())
    print(user3.getGroups())
