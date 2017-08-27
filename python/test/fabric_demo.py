#!/usr/bin/env python
#coding:utf-8

from fabric.api import *

env.user = 'root'
env.hosts= ['172.16.10.54','172.16.10.53']
env.password = '123456'

# 查看本地系统,当有多台主机时,只运行一次
@runs_once
# 本地系统函数
def local_task():
        local('uname -a')

def remote_task():
        # 'with'的作用是让后面的表达式的语句继承当前状态,实现'cd /home && ls -l'的效果
        with cd('/home'):
                run('ls -l')