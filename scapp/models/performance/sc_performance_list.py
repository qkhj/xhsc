#coding:utf-8
__author__ = 'hejia'

from scapp import db
import datetime

class SC_performance_list(db.Model):
    '''
    业绩表
    '''
    __tablename__ = 'sc_performance_list'
    id = db.Column(db.Integer, primary_key=True)
    month=db.Column(db.String(11))#月份
    manager_id=db.Column(db.String(11))#员工工号
    count=db.Column(db.Integer)#折算笔数
    valid_sum=db.Column(db.Integer)#有效管数
    month_rest=db.Column(db.String(11))#当月利息


    def __init__(self,month,manager_id,count,valid_sum,month_rest):
    	self.month = month
    	self.manager_id = manager_id
    	self.count = count
    	self.valid_sum = valid_sum
    	self.month_rest = month_rest


	def add(self):
		db.session.add(self)