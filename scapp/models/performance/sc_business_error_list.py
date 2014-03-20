#coding:utf-8
__author__ = 'hejia'

from scapp import db
import datetime

class SC_business_error_list(db.Model):
    '''
    业务差错统计
    '''
    __tablename__ = 'sc_business_error_list'
    id = db.Column(db.Integer, primary_key=True)
    manager_id=db.Column(db.String(11))#员工工号
    create_time=db.Column(db.String(11))#记录时间
    error_reason=db.Column(db.String(300))#差错原因
    create_person=db.Column(db.String(11))#记录人


    def __init__(self,manager_id,create_time,error_reason,create_person):
    	self.manager_id = manager_id
    	self.create_time = create_time
    	self.error_reason = error_reason
    	self.create_person = create_person


	def add(self):
		db.session.add(self)