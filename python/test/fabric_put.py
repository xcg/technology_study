#!/usr/bin/env python
#coding:utf-8

from fabric.api import *
from fabric.context_managers import *
from fabric.contrib.console import confirm

env.user = 'root'

# 定义堡垒机IP，作为文件上传，执行的中转
env.gateway = '172.16.10.53'

env.hosts = ['172.16.10.54','172.16.10.55']

# 假如所有主机密码都不一样，可以通过env.passwords字典变量一一指定
env.passwords = {
        'root@172.16.10.54':'123456',
        'root@172.16.10.55':'123456',
        'xuchanggang@172.16.10.53':'xuchanggang'
}

# 本地安装包路径
lpackpath = '/tmp/backup_log.tar.gz'

# 远程安装包路径
rpackpath = '/tmp/install'

@task
def put_task():
        run('mkdir -p /tmp/install')
        with settings(warn_only=True):
                result = put(lpackpath,rpackpath)
        if result.failed and not confirm('put file failed,Continue[Y/N]？'):
                abort('Aborting file put task!!')

@task
def run_task():
        with cd('/tmp/install'):
                run('tar -xf backup_log.tar.gz')
                with cd('backup_log/'):
                        run('echo 1 > 1.txt')

@task
def go():
        put_task()
        run_task()