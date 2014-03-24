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
    manager_name=db.Column(db.String(11))#员工名称
    create_time=db.Column(db.DateTime)#记录时间
    error_reason=db.Column(db.String(300))#差错原因


    def __init__(self,manager_id,manager_name,create_time,error_reason):
    	self.manager_id = manager_id
        self.manager_name = manager_name
    	self.create_time = create_time
    	self.error_reason = error_reason

    def add(self):
        db.session.add(self)