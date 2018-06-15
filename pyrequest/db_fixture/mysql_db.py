#!/usr/bin/env python
# encoding: utf-8
'''
@author: Sally
@time: 2018/6/14 23:00
'''
from pymysql import cursors, connect
from pymysql.err import OperationalError
import os
from configparser import ConfigParser

#=========读取数据库db_conf.ini 文件设置=============
base_dir = str(os.path.dirname(os.path.dirname(__file__)))  # 获取当前文件的上级目录的上级目录的路径
file_path = base_dir + "/db_config.ini"
cf = ConfigParser()
cf.read(file_path)

host = cf.get("mysqlconf", "host")
port = cf.get("mysqlconf", "port")
db = cf.get("mysqlconf", "db_name")
user = cf.get("mysqlconf", "user")
password = cf.get("mysqlconf", "password")
#=========封装mysql基本操作=========================
# class DB:
