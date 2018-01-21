#!/usr/bin/python
# -*- coding: utf-8 -*-  

import MySQLdb
import os
import datetime

def get_db_role(host,port):
        try:
          remote_conn=MySQLdb.connect(host=Remote_Mysql_Host,user=Remote_Mysql_User,passwd=Remote_Mysql_Pwd,db=Remote_Database,charset="utf8",port=Remote_Mysql_Port)
        except Exception,cnn_e:
          print cnn_e
        remote_cur=remote_conn.cursor()
        remote_sql="select master_slave from resources_instance where lanip='%s' and port=%s and service='mysqld'" % (host,port)
        #print remote_sql
        try:
          rows=remote_cur.execute(remote_sql)
          if rows > 0:
            results=remote_cur.fetchone()
            for row in results:
              if row[0] == 'M':
                DB_Role=1
              else:
                DB_Role=0
          else:
            DB_Role=0
          remote_conn.close()
          return DB_Role
        except Exception,desc_err:
          print str(desc_err)

def get_capacity_table_pre(host,port,schema_name,table_name,capacity_date_pre):
        try:
          remote_conn=MySQLdb.connect(host=Remote_Mysql_Host,user=Remote_Mysql_User,passwd=Remote_Mysql_Pwd,db=Remote_Database,charset="utf8",port=Remote_Mysql_Port)
        except Exception,cnn_e:
          print cnn_e
        remote_cur=remote_conn.cursor()
        remote_sql="select table_rows,table_size,chip_size from capacity_table_pre where host_ip='%s' and host_port=%s and schema_name='%s' and table_name='%s' and capacity_date='%s'" % (host,port,schema_name,table_name,capacity_date_pre)
        #print remote_sql
        try:
          rows=remote_cur.execute(remote_sql)
          if rows >0:
            pre_results=remote_cur.fetchone()
          else:
            pre_results=0
          remote_conn.close()
          return pre_results
        except Exception,desc_err:
          print str(desc_err)

def delete_repeat_capacity_data(host,port,schema_name,table_name,capacity_date,capacity_date_pre):
        try:
          remote_conn=MySQLdb.connect(host=Remote_Mysql_Host,user=Remote_Mysql_User,passwd=Remote_Mysql_Pwd,db=Remote_Database,charset="utf8",port=Remote_Mysql_Port)
        except Exception,cnn_e:
          print cnn_e
        remote_cur=remote_conn.cursor()
        capacity_table_pre_repeat_sql="delete from capacity_table_pre where host_ip='%s' and host_port=%s and schema_name='%s' and table_name='%s' and capacity_date='%s'" % (host,port,schema_name,table_name,capacity_date)
        capacity_table_pre_history_sql="delete from capacity_table_pre where host_ip='%s' and host_port=%s and schema_name='%s' and table_name='%s' and capacity_date<'%s'" % (host,port,schema_name,table_name,capacity_date_pre)
        capacity_table_repeat_sql="delete from capacity_table where host_ip='%s' and host_port=%s and schema_name='%s' and table_name='%s' and capacity_date='%s'" % (host,port,schema_name,table_name,capacity_date)
        #print capacity_table_pre_sql
        #print capacity_table_sql
        try:
          remote_cur.execute(capacity_table_pre_repeat_sql)
          remote_cur.execute(capacity_table_pre_history_sql)
          remote_cur.execute(capacity_table_repeat_sql)
          remote_conn.commit()
          remote_conn.close()
        except Exception,desc_err:
          remote_conn.rollback()
          print str(desc_err)

def get_local_capacity_data():
        try:
          Local_conn=MySQLdb.connect(host=Local_Mysql_Host,user=Local_Mysql_User,passwd=Local_Mysql_Pwd,db=Local_Database,charset="utf8",port=Port)
        except Exception,cnn_e:
          print cnn_e
        Local_cur=Local_conn.cursor()
        Local_sql="SELECT table_schema,table_name,table_rows,(data_length+index_length) AS data_size,data_free FROM tables WHERE table_schema NOT IN ('information_schema','mysql','log','performance_schema','test','sys')"
        try:
          rows=Local_cur.execute(Local_sql)
          if rows>0:
            results = Local_cur.fetchall()
          else:
            results = 0
          Local_conn.close()
          return results
        except Exception,desc_err:
          print str(desc_err)

def insert_capacity_data(host,port,schema_name,table_name,capacity_date,table_rows,table_size,data_free,daily_incr_rows,daily_incr_size,daily_incr_chip):
        try:
          remote_conn=MySQLdb.connect(host=Remote_Mysql_Host,user=Remote_Mysql_User,passwd=Remote_Mysql_Pwd,db=Remote_Database,charset="utf8",port=Remote_Mysql_Port)
        except Exception,cnn_e:
          print cnn_e
        remote_cur=remote_conn.cursor()
        capacity_table_pre_sql="insert into capacity_table_pre(capacity_date,host_ip,host_port,schema_name,table_name,table_rows,table_size,chip_size) values ('%s','%s','%s','%s','%s','%s','%s','%s')" % (capacity_date,host,port,schema_name,table_name,table_rows,table_size,data_free)
        capacity_table_sql="insert into capacity_table(capacity_date,host_ip,host_port,schema_name,table_name,table_rows,table_size,chip_size,daily_incr_rows,daily_incr_size,daily_incr_chip) values ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" % (capacity_date,host,port,schema_name,table_name,table_rows,table_size,data_free,daily_incr_rows,daily_incr_size,daily_incr_chip)
        #print capacity_table_pre_sql
        #print capacity_table_sql
        try:
          remote_cur.execute(capacity_table_pre_sql)
          remote_cur.execute(capacity_table_sql)
          remote_conn.commit()
          remote_conn.close()
        except Exception,desc_err:
          remote_conn.rollback()
          print str(desc_err)

if __name__ == '__main__':
        # Global Variables
        Remote_Mysql_Host='10.198.195.241'
        Remote_Mysql_User='devops'
        Remote_Mysql_Pwd='devops'
        Remote_Mysql_Port=3306
        Remote_Database='vipshop_dba'

        Local_Mysql_Host='10.198.195.241'
        Local_Mysql_User='dba'
        Local_Mysql_Pwd='localdba'
        Local_Database='information_schema'
        Local_All_Port=os.popen("ps -ef|grep /bin/mysqld|grep -v mysqld_safe|grep =$1|awk -F'port=' '{print $2}'|awk -F' ' '{print $1}'").read().strip('\n')            

        Capacity_Date_Now=datetime.date.today()
        Capacity_Date_Pre=datetime.date.today() - datetime.timedelta(days=1)
        
        Local_Ip=os.popen("grep -H IPADDR /etc/sysconfig/network-scripts/ifcfg-*0* | grep 'bond0[^:]*:IPADDR=\|eth0[^:]*:IPADDR=' | head -n 1 | sed 's/^.*IPADDR=//'").read().strip('\n')

        for Local_Port in Local_All_Port.split('\n'):
            Port=int(Local_Port)
            DB_Master=get_db_role(Local_Ip,Local_Port)
            #print DB_Master
            if DB_Master:
            #  purge_capacity_table_pre(Local_Ip,Local_Port,Schema_Name,Capacity_Date_Pre)
              capacity_results=get_local_capacity_data()
              if capacity_results>0:
                for capacity_result in capacity_results:
                    table_schema=capacity_result[0]
                    table_name=capacity_result[1]
                    table_rows=capacity_result[2]
                    data_size=capacity_result[3]
                    data_free=capacity_result[4]
                    delete_repeat_capacity_data(Local_Ip,Local_Port,table_schema,table_name,Capacity_Date_Now,Capacity_Date_Pre)
                    pre_results=get_capacity_table_pre(Local_Ip,Local_Port,table_schema,table_name,Capacity_Date_Pre)
                    if pre_results>0:
                      daily_incr_rows=table_rows-pre_results[0]
                      daily_incr_size=data_size-pre_results[1]
                      daily_incr_chip=data_free-pre_results[2]
                      #print table_schema,table_name,table_rows,data_size,data_free
                      #print daily_incr_rows,daily_incr_size,daily_incr_chip
                      #print '-------'
                    else:
                      daily_incr_rows=0
                      daily_incr_size=0
                      daily_incr_chip=0
                    insert_capacity_data(Local_Ip,Local_Port,table_schema,table_name,Capacity_Date_Now,table_rows,data_size,data_free,daily_incr_rows,daily_incr_size,daily_incr_chip)
              else:
                print 'no capacity data'
            else:
              print 'DB is not master'     
