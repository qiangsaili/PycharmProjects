#!/usr/bin/env python
# encoding: utf-8
'''
@author: Sally
@time: 2018/4/25 22:33
'''
import random
import string
import xlrd,xlwt
import csv
import pymysql


def Random_Active(lenght,num):
	#创建数据库连接
	conn = pymysql.connect(host='192.168.199.242', port=3306, user='root', password='iraindb10241GB', database='auto_test')
	#创建数据库游标
	cur = conn.cursor()
	#准备写入csv文件
	filehandle_csv = open('random_code.csv','a',newline= '')
	#准备写入xls文件
	filehandle_xls = xlwt.Workbook('random_code.xls')
	table = filehandle_xls.add_sheet('random_code')
	table.write(0,0,'num')
	table.write(0,1, 'active_code')
	#准备写入txt文件
	with open('random_code.txt', 'w') as filehandle_txt:
		i = 1
		while i < num:
			random_code = ''.join(random.sample(string.ascii_uppercase + string.digits + string.ascii_lowercase, lenght))
			print(random_code)
			#判断是否重复
			if not jude_repeat(random_code):
				print(jude_repeat(random_code))
				#写入TXT文件
				filehandle_txt.write(random_code + '\n')
				#写入xls文件
				table.write(i,0,i)
				table.write(i,1,random_code)
				#写入csv文件
				list = [i,random_code]
				filehandle_csv_write = csv.writer(filehandle_csv,dialect='excel')
				filehandle_csv_write.writerow(list)
				#写入数据mysql数据库
				sql = "insert into active_randoms(id,code_num)values(%d,\'%s\')" % (i,random_code)
				cur.execute(sql)
			else:
				i = i - 1
			i = i + 1
	filehandle_txt.close() #关闭TXT文件
	filehandle_xls.save('random_code.xls')#保存xls文件
	filehandle_csv.close() #关闭csv文件
	cur.close()
	conn.commit()
	conn.close()
	
def jude_repeat(context):
	file_read = open('random_code.txt', 'r')
	file_read_line = file_read.readlines()
	if context in file_read_line:
		return True
	else:
		return False
	
Random_Active(12,200)