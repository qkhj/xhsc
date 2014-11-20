#!/usr/bin/env python
# -*- coding: utf-8 -*-

import MySQLdb
from scapp.config import logger 

class DBHelp():
	def __init__(self):
		# 使用cursor()方法获取操作游标 
		self.db = MySQLdb.connect(host="127.0.0.1",user="root",passwd="root",db="sc_schema",charset="utf8")
		self.cursor = self.db.cursor()
	
	def executeSql(self,sql,file):
		try:
		   # 执行sql语句
		   sql = sql.replace("\\","")
		   self.cursor.execute(sql)
		   # 提交到数据库执行
		   id = int(self.db.insert_id()) 
		   self.db.commit()
		   return id
		except Exception,ex: 
		   # Rollback in case there is any error
		   loginfo = "%s-%s-%s" % (file.decode("gbk"),ex,sql)
		   logger.info(loginfo)
		   self.db.rollback()
		   return -1
		   
	def closeDB(self):
		# 关闭数据库连接
		self.db.close()