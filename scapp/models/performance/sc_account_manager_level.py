#coding:utf-8
__author__ = 'hejia'

from scapp import db
import datetime

class SC_account_manager_level(db.Model):
    '''
    客户经理层级表
    '''
    __tablename__ = 'sc_account_manager_level'
    id = db.Column(db.Integer, primary_key=True)
    level_id=db.Column(db.String(11))#客户经理级别
    level_name=db.Column(db.String(11))#级别名称

    def __init__(self,level_id,level_name):
    	self.level_id = level_id
    	self.level_name = level_name

	def add(self):
		db.session.add(self)