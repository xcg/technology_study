#!/usr/bin/env python
#coding:utf-8

from fabric.api import *

env.user = 'root'
env.hosts= ['172.16.10.54','172.16.10.53']
env.password = '123456'

@runs_once
def input_raw():
        return prompt('please input directory name:',default='/home')

def worktask(dirname):
        run('ls -l '+dirname)

@task
def go():
        getdirname = input_raw()
        worktask(getdirname)