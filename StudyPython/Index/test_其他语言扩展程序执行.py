#!/usr/bin/env python
# coding:utf8

import os

# system(cmd)    执行一个用cmd字符串表示的命令，返回命令执行结果状态码（对于windows系统总返回0）
# fork() 创建一个与父进程同级的子进程，[通常与exec*（）一起使用]，返回两次结果，一次为父进程，一次为子进程
# execl(file, arg0, arg1, ...) 执行一个可执行文件，并带上参数
# execv(file, arglist) 与execl()相同， 除了参数列表使用list，tunple传递
# execle(file, arg0, arg1, ...env) 与execl()相同， 同时还提供执行时的环境变量
# execve(file, arglist, env) 与execle()相同， 除了参数列表使用list，tunple传递
# execlp(cmd, arg0, arg1,...) 与execl()相同， 但可以从PATH环境变量中搜索命令（可执行文件）的完整路径
# execvp(cmd, arglist) 与execlp()相同，除了参数列表使用list，tunple传递
# execlpe(cmd, arg0, arg1,...env) 与execlp()相同，同时还提供执行时的环境变量
# execvpe(cmd, arglist, env) 与execvp()相同，同时还提供执行时的环境变量
# spawn*(mode, file, args[, env])
# family executes path in a new process given args as
# arguments and possibly an environment variable dictionary env;
# mode is a magic number indicating various modes of operation
# wait() 等待子进程完成 [通常与fork() 和exec*()一起使用]
# waitpid(pid, options) 等待指定pid的子进程完成 [通常与fork() 和exec*()一起使用]
# popen*(cmd, mode='r ', buffering=-1) 执行一个字符串表示的命令, 返回一个类文件对象用于进程间通信，默认为只读模式并使用系统提供的缓冲
# startfile(path) 执行与path相关联的应用

import sys
print >> sys.stderr, 'error result print'

import commands
tup = commands.getstatusoutput('dir')
print tup