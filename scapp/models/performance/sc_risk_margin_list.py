#coding:utf-8
__author__ = 'hejia'

from scapp import db
import datetime

class SC_risk_margin_list(db.Model):
    '''
    风险保证金详单
    '''
    __tablename__ = 'sc_risk_margin_list'
    id = db.Column(db.Integer, primary_key=True)
    manager_id=db.Column(db.Integer)#员工工号
    payment_time=db.Column(db.DateTime)#工资时间
    inout_payment=db.Column(db.String(11))#进出金额
    inout_type=db.Column(db.Integer)#1-新增，2-逾期，3-返还
    last_margin=db.Column(db.String(11))#剩余保证金

    def __init__(self,manager_id,payment_time,inout_payment,inout_type,last_margin):
    	self.manager_id = manager_id
    	self.payment_time = payment_time
    	self.inout_payment = inout_payment
    	self.inout_type = inout_type
        self.last_margin = last_margin

    def add(self):
        db.session.add(self)