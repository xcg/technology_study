# /usr/bin/env python
# coding:utf-8
# author:Michael.Xu
# info:获取主机名，主机系统，系统版本

import platform
import os

# 获取方式:
# 1.使用platform

def get_os_info_platform():
        all_info = platform.uname()
        os_type = all_info[0]
        os_hostname = all_info[1]
        os_kernel = all_info[2]
        print all_info
        print '-----------------'
        print os_type,os_hostname,os_kernel 
        print '+++++++++++++++++'

        os_tyoe1 = platform.system()
        os_system = platform.linux_distribution()[0]
        os_version = platform.linux_distribution()[1] 
        os_hostname1 = platform.node()
        os_kernel1 = platform.release() 
        print os_tyoe1,os_system,os_version, os_hostname1,os_kernel1 
        print '+++++++++++++++++'


# 2.使用os
def get_osinfo():
        os_info = {}
        i = os.uname()
        os_info['os_type'] = i[0]
        os_info['node_name'] = i[1]
        os_info['kernel'] = i[2]
        print os_info['os_type'], os_info['node_name'],os_info['kernel']
        return os_info




get_os_info_platform()

get_osinfo()