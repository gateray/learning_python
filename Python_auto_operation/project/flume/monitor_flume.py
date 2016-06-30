#!/usr/bin/env python
# coding: utf-8

from os import popen
import thread

class MyProcess:
    def __init__(self,pid=None,cmd=None,owner=None,cpu=None,mem=None,rsize=None,vsize=None,start=None,time=None,tty=None,stat=None):
        """
        USER       PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
        'root     15858 18.1 37.2 4719600 2999404 ?     Sl   Jan03 496:45 /data/mongodb/bin/mongod --shardsvr --replSet shard2 --port 26002 --dbpath=/data/shard'
        """
        self.pid = pid
        self.cmd = cmd
        self.owner = owner
        self.cpu = cpu
        self.mem = mem
        self.rsize = rsize
        self.vsize = vsize
        self.start = start
        self.time = time
        self.tty = tty
        self.stat = stat
    def __eq__(self, other):
        return self.pid.__eq__(other.pid) or self.cmd.__eq__(other.cmd)
    def __hash__(self):
        return hash(self.cmd)

class CheckProcess:
    def __init__(self,cmd,servicename):
        self.cmd = cmd
        self.servicename = servicename
        self.pset = self.getProcesses(cmd)
        self.lastprocessinfo = self.pset
    def exist(self,process):
        return process in self.pset
    def getProcesses(self,cmd):
        po = popen(cmd)
        out = po.read().strip()
        po.close()
        plineset = set(out.split("\n"))
        pset = set()
        for pline in plineset:
            fields= pline.split()
            pset.add(MyProcess(owner=fields[0],
                                  pid=fields[1],
                                  cpu=fields[2],
                                  mem=fields[3],
                                  vsize=fields[4],
                                  rsize=fields[5],
                                  tty=fields[6],
                                  stat=fields[7],
                                  start=fields[8],
                                  time=fields[9],
                                  cmd=" ".join(fields[10:])))
        return pset
    def start(self,process):
        out = popen(process.cmd + "&& echo 0 || echo 1").read().strip()
    def monitor(self):
        import time
        #-----debug------
        for p in self.pset:
            print(p.cmd)
        #-----debug------
        while True:
            cur_pset = self.getProcesses(self.cmd)
            if len(cur_pset) != len(self.pset):
                dif_set = self.pset.difference(cur_pset)
                # for process in dif_set:
                #     self.start(process)
                #self.mail(self.lastprocessinfo.intersection(dif_set))
                thread.start_new_thread(self.mail,(self.lastprocessinfo.intersection(dif_set),))
            else:
                self.lastprocessinfo = cur_pset
            time.sleep(30)
    def mail(self,pset):
        from emailutil import EMailUtil
        subject = "Report \"" + self.servicename + u"\" Service Fall"
        from_addr = "admin@smtp.gizwits.com"
        to_list = ["ops@xtremeprog.com"]
        #to_list = ["gwzhou@gizwits.com"]
        smtpserver = "10.221.28.207"
        eu = EMailUtil(subject,from_addr,to_list)
        out = popen("hostname")
        hostname = out.read().strip()
        out.close()
        eu.addMessage("Host: " + hostname + "\n")
        for i,process in enumerate(pset):
            eu.addMessage(
                "    Process{0} last info:\n".format(i+1) +
                "        command: " + process.cmd + "\n"
                "        owner: " + process.owner + "\n"
                "        pid: " + process.pid + "\n"
                "        cpu%: " + process.cpu + "\n"
                "        mem%: " + process.mem + "\n"
                "        reside_mem_used(KB):" + process.rsize + "\n"
                "        virtual_mem_used(KB):" + process.vsize + "\n"
                "        starttime:" + process.start + "\n"
                "        cputime:" + process.time + "\n\n"
            )
        eu.addMessage("-----------------end-----------------\n")
        eu.sendmail(smtpserver)
        print("send mail.")
        thread.exit_thread()

if __name__ == "__main__":
    CheckProcess("ps aux | grep '.*java.*flume.*rt01' | grep -v 'grep'",servicename="Flume").monitor()
