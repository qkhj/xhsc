#coding:utf-8
__author__ = 'hejia'

from scapp import db
import datetime

class SC_manager_level_index(db.Model):
    '''
    客户经理层级指标
    '''
    __tablename__ = 'sc_manager_level_index'
    id = db.Column(db.Integer, primary_key=True)
    level_id=db.Column(db.Integer)#客户经理级别
    valid_sum=db.Column(db.Integer)#有效管户数
    balance_scale=db.Column(db.String(11))#余额规模
    count=db.Column(db.String(11))#折算笔数

    def __init__(self,level_id,valid_sum,balance_scale,count):
    	self.level_id = level_id
    	self.valid_sum = valid_sum
    	self.balance_scale = balance_scale
    	self.count = count


	def add(self):
		db.session.add(self)