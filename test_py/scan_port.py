#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys
import nmap

scan_row=[]
input_data = raw_input('Please input hosts and port: ')
scan_row = input_data.split(" ")
if len(scan_row)!=2: 
	print "Input errors,example \"192.168.1.0/24 80,443,22\""
	sys.exit(0)

# 接收用户输入的主机
hosts=scan_row[0] 

# 接收用户输入的端口
port=scan_row[1] 

try:
  # 创建端口扫描对象
	nm = nmap.PortScanner()
except nmap.PortScannerError:
	print('Nmap not found', sys.exc_info()[0])
	sys.exit(0)
except:
	print("Unexpected error:", sys.exc_info()[0])
	sys.exit(0)

try:
	# 调用扫描方法,参数指定扫描主机hosts,nmap扫描命令行参数arguments
	nm.scan(hosts=hosts, arguments=' -v -sS -p '+port)
except Exception,e:
	print "Scan erro:"+str(e)

# 遍历扫描主机
for host in nm.all_hosts(): 
	print('----------------------------------------------------')

	# 输出主机及主机名
	print('Host : %s (%s)' % (host, nm[host].hostname()))
	
	# 输出主机状态,如up、down
	print('State : %s' % nm[host].state())
	
	# 遍历扫描协议,如tcp、udp
	for proto in nm[host].all_protocols(): 
		print('----------')
		
		# 输入协议名 
		print('Protocol : %s' % proto) 
		
		# 获取协议的所有扫描端口
		lport = nm[host][proto].keys() 
		
		# 端口列表排序
		lport.sort() 
		for port in lport: 
		  # 遍历端口及输出端口与状态
			print('port : %s\tstate : %s' % (port, nm[host][proto][port]['state']))