#!/usr/bin/env python
# encoding: utf-8
'''
@author: Sally
@time: 2018/5/8 22:08
'''

from pymysql import cursors, connect

#连接数据库
conn = connect('127.0.0.1',
               user='root',
               password='root123456',
               db='guest',
               charset='utf8mb4',
               cursorclass=cursors.DictCursor)
try:
	with conn.cursor() as cursors:
		#创发布会数据
		sql = 'INSERT INTO sign_event(id, name, limite, status, start_time, create_time, address) VALUES' \
		    '(1,"iPhone X发布会", 1000, 1, "2018-06-10 08:00:00", NOW(), "软件新城abc");'
		cursors.execute(sql)
	#提交事务
	conn.commit()
	with conn.cursor() as cursors:
		#创建嘉宾数据
		sql = 'INSERT INTO sign_guest(realname, phone, email, sign, event_id, create_time) VALUES' \
		    '("Tom",18701000000, "tom@mail.com", 0, 1, NOW());'
		cursors.execute(sql)
	#提交事务
	conn.commit()
	with conn.cursor() as cursors:
		#查询添加的嘉宾
		sql = "SELECT realname, phone, email, sign FROM sign_guest WHERE phone=%s"
		cursors.execute(sql, ('18701000000',))
		result = cursors.fetchone()
		print(result)
finally:
	conn.close()
