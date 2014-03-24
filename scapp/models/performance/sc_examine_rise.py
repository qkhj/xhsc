#coding:utf-8
__author__ = 'hejia'

from scapp import db
import datetime

class SC_examine_rise(db.Model):
    '''
    晋降级审核表
    '''
    __tablename__ = 'sc_examine_rise'
    id = db.Column(db.Integer, primary_key=True)
    manager_id=db.Column(db.String(11))#员工工号
    apply_time=db.Column(db.String(11))#申请时间
    apply_type=db.Column(db.String(11))#审核类型
    apply_result=db.Column(db.String(11))#审核结果

    def __init__(self,manager_id,apply_time,apply_type,apply_result):
    	self.manager_id = manager_id
    	self.apply_time = apply_time
    	self.apply_type = apply_type
    	self.apply_result = apply_result


	def add(self):
		db.session.add(self)