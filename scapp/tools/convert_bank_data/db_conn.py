# coding:utf-8
"""
数据库接口
"""
import config

__author__ = 'johhny'

import sqlalchemy

mysql_local_engine = sqlalchemy.create_engine(config.SQLALCHEMY_LOCAL_DATABASE_URI)
#获得连接
local_db_conn = mysql_local_engine.connect()

