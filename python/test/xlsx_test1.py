#!/usr/bin/env python
#coding:utf-8

import xlsxwriter

workbook = xlsxwriter.Workbook('demo1.xlsx')
worksheet = workbook.add_worksheet()
worksheet.set_column('A:A',20)
bold = workbook.add_format({'bold':True})
worksheet.write('A1','HELLO')
worksheet.write('A2','WORLD',bold)
worksheet.write('B2',u'中文测试',bold)

# 相当于A3,以0为起始
worksheet.write(2,0,32)

# 相当于A4,以0为起始
worksheet.write(3,0,35.5)
worksheet.write(4,0,'=sum(A3:A4)')
workbook.close()