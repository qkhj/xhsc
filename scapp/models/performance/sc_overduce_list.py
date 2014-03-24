#coding:utf-8
__author__ = 'hejia'

from scapp import db
import datetime

class SC_overduce_list(db.Model):
    '''
    逾期单详情
    '''
    __tablename__ = 'sc_overduce_list'
    id = db.Column(db.Integer, primary_key=True)
    loan_apply_id=db.Column(db.String(11))#贷款编号
    now_month=db.Column(db.String(11))#当前月份
    pay_time=db.Column(db.String(11))#应还日期
    overduce_payment=db.Column(db.String(11))#逾期金额
    manager_id=db.Column(db.String(11))#员工工号

    def __init__(self,loan_apply_id,now_month,pay_time,overduce_payment,manager_id):
    	self.loan_apply_id = loan_apply_id
    	self.now_month = now_month
    	self.pay_time = pay_time
    	self.overduce_payment = overduce_payment
        self.manager_id = manager_id

	def add(self):
		db.session.add(self)