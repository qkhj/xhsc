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
    assess_type=db.Column(db.String(11))#评估类型
    assess_result=db.Column(db.String(11))#评估结果

    def __init__(self,manager_id,assess_time,assess_type,assess_result):
    	self.manager_id = manager_id
    	self.assess_time = assess_time
    	self.assess_type = assess_type
    	self.assess_result = assess_result

	def add(self):
		db.session.add(self)