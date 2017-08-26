# /usr/bin/env python
# coding:utf-8
# author:Michael.Xu
# info:get os information

import os
import psutil
import platform
import datetime
import socket
import uuid

#对字典取子集
def sub_dict(form_dict, sub_keys, default=None):
    return dict([(k, form_dict.get(k.strip(), default)) for k in sub_keys.split(',')])


# 获取主机CPU核数，个数(逻辑/物理)，主频，型号
def read_cpuinfo():
        cpu_stat = []
        with open('/proc/cpuinfo', 'r') as f:
                data = f.read()
                for line in data.split('\n\n'):
                        cpu_stat.append(line)
        return cpu_stat[-2]

def get_cpuinfo(data):
        cpu_info = {}
        for i in data.splitlines():
                # x.strip(rm): 当 rm 为空时，默认删除开头,结尾空白符(包括'\n','\r','\t',' ')
                k, v = [ x.strip() for x in i.split(':')]
                cpu_info[k] = v
                # print cpu_info[k]
        cpu_info['physical id'] = str(int(cpu_info.get('physical id')) + 1)
        #cpu_cores = cpu_info['cpu cores']
        #cpu_physical_counts = cpu_info['physical id']
        #cpu_logic_counts = int(cpu_cores) * int(cpu_physical_counts)
        #cpu_type = cpu_info['model name']
        #print 'CPU核数: %s' % cpu_info['cpu cores']
        #print 'CPU个数(物理): %s' % cpu_info['physical id']
        #print 'CPU型号: %s' % cpu_info['model name']
        #return sub_dict(cpu_info, 'model name,physical id,cpu cores')
        return cpu_info 

# 获取内存、swap信息
def get_meminfo():
        mem_info = {}
        m = psutil.virtual_memory()
        mem_info['mem_total'] = m.total/1000/1000/1000
        mem_info['mem_available'] = m.available/1000/1000/1000
        mem_info['mem_free'] = m.free/1000/1000/1000
        mem_info['mem_use_rate'] = m.percent

        s = psutil.swap_memory()
        mem_info['swap_total'] = s.total/1000/1000/1000
        mem_info['swap_free'] = s.free/1000/1000/1000
        mem_info['swap_use_rate'] = s.percent

        return mem_info

# 获取系统版本信息,主机开机时间,登录用户信息
def get_osinfo():
        os_info = {}
        os_info['os_type'] =  platform.system()
        os_info['os_system'] = platform.linux_distribution()[0]
        os_info['os_version'] = platform.linux_distribution()[1]
        os_info['os_kernel'] =  platform.release()
        os_info['os_hostname'] = platform.node()
        os_info['os_starttime'] = datetime.datetime.fromtimestamp(psutil.boot_time()).strftime("%Y-%m-%d %H:%M:%S")  
        os_info['users_count'] = len(psutil.users())
        os_info['users_list'] = ",".join([u.name for u in psutil.users()])
        os_info['users_host'] = ",".join([u.host for u in psutil.users()])

        return os_info


# 获取磁盘信息
def get_diskinfo():
        disk_info = []
        disk_partitions = psutil.disk_partitions()
        for i in disk_partitions:
                partitions_info = {}
                partitions_info['device'] = i[0]
                partitions_info['mount'] = i[1]
                partitions_info['fstype'] = i[2]
                mount = partitions_info['mount']

                capacity = psutil.disk_usage(partitions_info['mount'])

                partitions_info['total_capacity'] = capacity.total/1000/1000/1000
                partitions_info['used_capacity'] = capacity.used/1000/1000/1000
                partitions_info['free_capacity'] = capacity.free/1000/1000/1000
                partitions_info['used_rate'] = capacity.percent
                #print "挂载点: %s 分区：%s 分区类型：%s 分区总大小：%s GB 分区已使用大小：%s GB 分区未使用大小：%s GB  使用率: %s" %(partitions_info['mount'],partitions_info['device'] ,partitions_info['fstype'],partitions_info['total_capacity'],partitions_info['used_capacity'],partitions_info['free_capacity'],partitions_info['used_rate'])
                disk_info.append(partitions_info)
        return disk_info


# 获取主机IP地址方式 #
def get_netinfo():
        net_info = {}
        hostname = socket.gethostname()
        mac = uuid.UUID(int = uuid.getnode()).hex[-12:]
        #mac_info =  ":".join([mac[e:e+2] for e in range(0,11,2)])
        net_info['ip'] = socket.gethostbyname(hostname)
        net_info['mac'] = ":".join([mac[e:e+2] for e in range(0,11,2)])
        return net_info


if __name__ == "__main__":
        rate = '%'
        cpu_info = get_cpuinfo(read_cpuinfo())
        os_info = get_osinfo()
        mem_info = get_meminfo()
        disk_info = get_diskinfo()
        net_info = get_netinfo()
        print '----- 系统信息 -----'
        print '系统类型: %s' % os_info['os_type']
        print '当前系统: %s %s ' % (os_info['os_system'],os_info['os_version'])
        print '系统内核版本: %s' % os_info['os_kernel']
        print '主机名: %s' % os_info['os_hostname']
        print '系统开始时间：%s' % os_info['os_starttime']
        print '当前登录用户数：%s' % os_info['users_count']
        print '当前登录用户分别为：%s' % os_info['users_list']
        print '用户来源IP分别为：%s' % os_info['users_host']
        print '----- CPU信息 -----'
        print 'CPU核数: %s' % cpu_info['cpu cores']
        print 'CPU个数(物理): %s' % cpu_info['physical id']
        print 'CPU型号: %s' % cpu_info['model name']
        print '----- 内存信息 -----'
        print '内存总计: %s GB' % mem_info['mem_total']
        print '有效内存: %s GB' % mem_info['mem_available']
        print '空闲内存: %s GB' % mem_info['mem_free']
        print '已使用内存占比: %s%s' % (mem_info['mem_use_rate'],rate)
        print 'SWAP内存总计：%s GB' % mem_info['swap_total']
        print 'SWAP空闲内存：%s GB' % mem_info['swap_free']
        print 'SWAP已使用内存占比：%s%s' % (mem_info['swap_use_rate'],rate)
        print '----- 磁盘信息 -----'
        for i in range(0,len(disk_info)):
                partitions_info = disk_info[i]
                #for k,v in partitions_info.items():
                #       print k,v
                print "挂载点: %s 分区：%s 分区类型：%s 分区总大小：%s GB 分区已使用大小：%s GB 分区未使>用大小：%s GB  使用率: %s" %(partitions_info['mount'],partitions_info['device'] ,partitions_info['fstype'],partitions_info['total_capacity'],partitions_info['used_capacity'],partitions_info['free_capacity'],partitions_info['used_rate'])
        print '----- 网卡信息 -----'
        print '本机IP地址为：%s' % net_info['ip']
        print '本机网卡MAC地址为：%s' % net_info['mac']
        print '----- 检测 结束 -----'