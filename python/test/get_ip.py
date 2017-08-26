# /usr/bin/env python
# coding:utf-8
# author:Michael.Xu
# info:获取主机IP地址

# 获取主机IP/MAC地址的方式:
# 1.使用SOCKET,uuid

import socket
import uuid
import re
import subprocess


def IP_socket():
        hostname = socket.gethostname()
        ip = socket.gethostbyname(hostname)
        print ip

def MAC_uuid():
        mac = uuid.UUID(int = uuid.getnode()).hex[-12:]
        return ":".join([mac[e:e+2] for e in range(0,11,2)])

IP_socket()
mac = MAC_uuid()
print mac

# 2.使用ifconfig截取实现
#读取ifconfig信息,p.communicate()[0],[0]去除None值,shell=True,是指使用shell特性执行
def read_ifconfig():
    p = subprocess.Popen('ifconfig', stdout=subprocess.PIPE, shell=True)
    return p.communicate()[0]

#返回网卡及ip信息：网卡、IP址、MAC地址
def get_ipinfo(data):
    data = (i for i in data.split('\n\n') if i and not i.startswith('lo'))    
    ip_info = []
    ifname = re.compile(r'(eth[\d:]*|wlan[\d:]*)')
    ipaddr = re.compile(r'(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[0-9]{1,2})(\.(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[0-9]{1,2})){3}')
    macaddr = re.compile(r'[A-F0-9a-f:]{17}')
    for i in data:
        x = {}
        if ifname.match(i):
            device = ifname.match(i).group()
            x['Adapter'] = device
        if macaddr.search(i):
            mac = macaddr.search(i).group()
            x['MAC'] = mac
        if ipaddr.search(i):
            ip = ipaddr.search(i).group()
            x['IP'] = ip
        else:
            x['IP'] = None
        ip_info.append(x)
    return ip_info

ipinfo = get_ipinfo(read_ifconfig())

print ipinfo[0]
print ipinfo[1]