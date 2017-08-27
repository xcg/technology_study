#!/usr/bin/env python
# coding:utf-8
# author:Michael.Xu
# INFO: SEND HOST PERFORMANCE IMAGE
# 图片大小需要控制好，统一大小 

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

HOST = 'smtp.163.com'
SUBJECT = u'主机性能数据报表'
TO = 'xuchanggang@163.com'
FROM = 'monitor@163.com'
USER = 'monitor@163.com'
PASSWORD = '123456'

def addimg(src,imgid):
        fp = open(src,'rb')
        msgImage = MIMEImage(fp.read())
        fp.close()
        msgImage.add_header('Content-ID',imgid)
        return msgImage

msg = MIMEMultipart('related')

msgtext = MIMEText("""
<img>
<table width='600' border='0' cellspacing='0' cellpadding='4'>
        <tr bgcolor='#CECFAD' height='20'>
                <td colspan=2>*官网性能数据 <a href='#'>更多>></a></td>
        </tr>
        <tr bgcolor='#EFEBDE' height='100'>
                <td><img src='cid:io'></td>
                <td><img src='cid:key_hit'></td>
        </tr>
        <tr bgcolor='#EFEBDE' height='100'>
                <td><img src='cid:mem'></td>
                <td><img src='cid:swap'></td>
        </tr>
</table>""","html","utf-8")

msg.attach(msgtext)
msg.attach(addimg('img/io.png','io'))
msg.attach(addimg('img/key_hit.png','key_hit'))
msg.attach(addimg('img/mem.png','mem'))
msg.attach(addimg('img/swap.png','swap'))

msg['Subject'] = SUBJECT
msg['From']     = FROM
msg['To'] = TO

try:
        server = smtplib.SMTP()
        server.connect(HOST,'25')
        server.login(USER,PASSWORD)
        server.sendmail(FROM,TO,msg.as_string())
        server.quit()
        print '邮件发送成功!!'
except Exception,e:
        print '失败:'+str(e)