#!/usr/local/bin/python 
#coding: utf-8 
# -*- coding: utf-8 -*-
# __author__ = 'Michael.Xu'

import MySQLdb as mysql
import re
from datetime import datetime, timedelta
import smtplib
import sys
from email.mime.text import MIMEText

reload(sys)
sys.setdefaultencoding( "utf-8" )

def sendHtmlMail(mailcontent,myip):
  try:
    #yestoday=(datetime.now()-timedelta(days=1)).strftime("%Y-%m-%d")
    sender = 'xuchanggang@163.com'
    receiver = ['a123@163.com','b456@163.com','c789@163.com']
    cc_user = ['A01@163.com','B02@163.com']
    subject = '数据库慢SQL：前20个('+ week + '--' + today +')'
    smtpserver = 'smtp.163.com'
    username = 'xuchanggang@163.com'
    password = '123456'
    msg = MIMEText(mailcontent,'html','utf-8')
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = ";".join(receiver)
    msg['Cc'] = ";".join(cc_user)
    smtp = smtplib.SMTP()
    smtp.connect(smtpserver)
    smtp.login(username, password)
    # 针对 收邮件的人 和 抄送邮件的人 都是单个，用下面方法
    #smtp.sendmail(sender, [receiver, cc_user], msg.as_string())
    # 下面这个针对 收邮件的人 和 抄送邮件的人 都是多个，都是列表时，用下面方法
    smtp.sendmail(sender,receiver+cc_user,msg.as_string())
    smtp.quit()
  except Exception, e:
    print e,'send mail error'
if __name__=='__main__':
  result=None
  htmlfile='mysqlSlowMon.html'
  myiplist=['127.0.0.1']
  week=(datetime.now()-timedelta(days=7)).strftime("%Y-%m-%d 00:00:00")
  today=datetime.now().strftime("%Y-%m-%d 00:00:00")
  #print week,today
  for myip in myiplist:
    sql="select SUM(ts_cnt),left(SUM(Query_time_sum)/SUM(ts_cnt),5),source.first_seen,source.last_seen,history.sample,CHECKSUM FROM  slow_query.global_query_review AS source JOIN slow_query.global_query_review_history AS history USING (CHECKSUM) WHERE history.ts_min >='%s' AND history.ts_min <'%s' GROUP BY history.checksum ORDER BY sum(ts_cnt) DESC LIMIT 20" %(week,today)
    try:
      dbcon = mysql.connect(host='127.0.0.1', user='root', passwd='123456, db='slow_query', port=3306,charset='utf8')
      cur = dbcon.cursor()
      print "step 1,"+myip+','+datetime.now().strftime("%Y-%m-%d %H:%M:%S")
      cur.execute(sql)
      result = cur.fetchall()
      cur.close()
      dbcon.close()
    except Exception, e:
      print e,'conn mysql error'
    print "step 2,"+myip+','+datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if result:
      headhtml='''<!DOCTYPE html><html class=" MacOS"><head><meta http-equiv="Content-Type" content="text/html; charset=utf-8"/><style type="text/css">
     #customers {
      FONT-FAMILY: "Trebuchet MS", Arial, Helvetica, sans-serif; BORDER-COLLAPSE: collapse
    }
     #customers TD {
      BORDER-TOP: #98bf21 1px solid; BORDER-RIGHT: #98bf21 1px solid; BORDER-BOTTOM: #98bf21 1px solid; PADDING-BOTTOM: 2px; PADDING-TOP: 3px; PADDING-LEFT: 7px; BORDER-LEFT: #98bf21 1px solid; PADDING-RIGHT: 7px
    }
     #customers TH {
      BORDER-TOP: #98bf21 1px solid; BORDER-RIGHT: #98bf21 1px solid; BORDER-BOTTOM: #98bf21 1px solid; PADDING-BOTTOM: 2px; PADDING-TOP: 3px; PADDING-LEFT: 7px; BORDER-LEFT: #98bf21 1px solid; PADDING-RIGHT: 7px
    }
     #customers THEAD {
      FONT-SIZE: 1.0em; COLOR: #fff; PADDING-BOTTOM: 4px; TEXT-ALIGN: left; PADDING-TOP: 5px; BACKGROUND-COLOR: #a7c942
    }
     #customers TR.alt TD {
      COLOR: #000; BACKGROUND-COLOR: #eaf2d3
    }
    </style>
      </head><body>
       <table id="customers" align="center">
            <thead><tr align="left">
              <td>调用次数(周)</td>
              <td>查询时间</td>
              <td>首次发现时间</td>
              <td>最新发现时间</td>
              <td>慢SQL范例</td>
              <td>唯一标识</td>
            </tr></thead><tbody>'''
      with open(htmlfile,'w') as htmlfileobj:
        htmlfileobj.write(headhtml)
        htmlfileobj.flush()
      for count,query_avg_time,first_time,last_time,sql,checksum in result:
        sql=re.compile(r'(\/\*(\s|.)*?\*\/)').sub("",sql)[0:15000].replace(u"\x00",'').strip()
        if not sql or sql.strip()=='' or sql.strip()==' ':
          continue
        with open(htmlfile,'a') as htmlfileobj:
          tmpstring='<tr align="left"><td>'+str(count)+'</td><td>'+str(query_avg_time)+'</td><td>'+str(first_time)+'</td><td>'+str(last_time)+'</td><td>'+str(sql)+'</td><td>'+str(checksum)+'</td></tr>'
          htmlfileobj.write(tmpstring)
      with open(htmlfile,'a') as htmlfileobj:
        tmpline='''</tbody></table></html>'''
        htmlfileobj.write(tmpline)
      with open(htmlfile,'r') as htmlfileobj:
        mailcontent=htmlfileobj.read()
      print "step 3,"+myip+','+datetime.now().strftime("%Y-%m-%d %H:%M:%S")
      sendHtmlMail(mailcontent,myip)
    else:
      print 'sql result is None,exiting'
    print "step 4,"+myip+','+datetime.now().strftime("%Y-%m-%d %H:%M:%S")