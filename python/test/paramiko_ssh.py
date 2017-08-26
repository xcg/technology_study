#!/usr/bin/env python
#-*- coding:utf-8 -*-
# info:ssh远程连接

import paramiko

hostname = '172.16.10.54'
username = 'root'
passwd = '123456'

paramiko.util.log_to_file('syslogin.log')
ssh = paramiko.SSHClient()


# 获取客户端host_keys,默认~/.ssh/known_hosts,非默认路径需指定
#known_host="/root/.ssh/known_hosts"
#ssh.load_system_host_keys(known_host)

ssh.load_system_host_keys()

# 设置连接远程主机没有本地密钥或hostkeys对象时的策略，支持三种，这里重点讲：AutoAddPolicy
# AutoAddPolicy：自动添加主机名及主机密钥到本地hostkeys对象，并将其保存，不依赖ssh.load_system_host_keys()
# ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

ssh.connect(hostname=hostname,username=username,password=passwd)

stdin,stdout,stderr = ssh.exec_command('free -m')
print stdout.read()

stdout.readlines()

ssh.close()
