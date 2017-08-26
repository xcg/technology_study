#!/usr/bin/env python
#info: 相关输出信息输出到文件或日志

import pexpect
import sys

child = pexpect.spawn('ssh root@172.16.10.54')
fout = file('mylog.txt','w')
#child.logfile = fout
child.logfile = sys.stdout
child.expect("password:")
child.sendline("123456")
child.expect('#')
child.sendline('ls /home')
child.expect('#')