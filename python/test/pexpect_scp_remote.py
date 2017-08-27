#!/usr/bin/env python
#info:登录远程主机操作文件，并传输到本地

import pexpect
import sys

ip = '172.16.10.54'
user = 'root'
password = '123456'
traget_file = '/tmp/backup.log'
child = pexpect.spawn('/usr/bin/ssh',[user+'@'+ip])
fout = file('mylog.txt','w')
child.logfile = fout

try:
        child.expect('(?i)password')
        child.sendline(password)
        child.expect('#')
        child.sendline('tar -cvf /tmp/backup_log.tar.gz ' + traget_file)
        child.expect('#')
        print child.before
        child.sendline('exit')
        fout.close()
except EOF:
        print 'expect EOF'
except TIMEOUT:
        print 'expect timeout'

child = pexpect.spawn('/usr/bin/scp',[user+'@'+ip+':/tmp/backup_log.tar.gz ','/tmp'])
fout = file('mylog.txt','a')
child.logfile = fout
try:
        child.expect('(?i)password')
        child.sendline(password)
        child.expect(pexpect.EOF)
except EOF:
        print 'expect EOF'
except TIMEOUT:
        print 'expect timeout'