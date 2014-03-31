#coding:utf-8
__author__ = 'hejia'

from scapp import db
import datetime

class SC_assess_record(db.Model):
    '''
    评估记录表
    '''
    __tablename__ = 'sc_assess_record'
    id = db.Column(db.Integer, primary_key=True)
    manager_id=db.Column(db.String(11))#员工工号
    assess_time=db.Column(db.String(11))#评估时间
    assess_arg=db.Column(db.String(11))#最近评估平均分
    assess_sum=db.Column(db.String(11))#评估次数

    def __init__(self,manager_id,assess_time,assess_arg,assess_sum):
    	self.manager_id = manager_id
    	self.assess_time = assess_time
    	self.assess_arg = assess_arg
    	self.assess_sum = assess_sum

	def add(self):
		db.session.add(self)