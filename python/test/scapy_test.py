#!/usr/bin/env python
# -*- coding:utf-8 -*-
# info: traceroute


import os
import sys
import time
import subprocess
import warnings
import logging

# 屏蔽scapy无用告警
warnings.filterwarnings("ignore",category=DeprecationWarning)

# 屏蔽模块IPV6多余告警
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)

from scapy.all import traceroute

# 接受输入域名或IP
domains = raw_input('Please input one or more IP/domain: ')

target = domains.split(' ')

# 扫描端口列表
dport = [80]

if len(target) >= 1 and target[0] !='':
        # 启动路由追踪
        res,unans = traceroute(target,dport=dport,retry=-2)

        # 生成SVG矢量图形
        res.graph(target="> test.svg")

        time.sleep(1)

        # svg 转 png 格式
        subprocess.Popen("/usr/bin/convert test.svg test.png",shell=True)

else:
        print "IP/domain number of errors,exit"