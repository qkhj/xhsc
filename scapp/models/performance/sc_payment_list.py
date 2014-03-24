#coding:utf-8
__author__ = 'hejia'

from scapp import db
import datetime

class SC_payment_list(db.Model):
    '''
    工资单
    '''
    __tablename__ = 'sc_payment_list'
    id = db.Column(db.Integer, primary_key=True)
    manager_id=db.Column(db.Integer)#员工工号
    manager_type=db.Column(db.Integer)#员工类型
    payment_time=db.Column(db.String(11))#工资时间
    position=db.Column(db.String(11))#职位
    base_payment=db.Column(db.String(11))#基本工资
    total_performance=db.Column(db.String(11))#所得总绩效
    assess_result=db.Column(db.String(11))#评估结果
    last_performance=db.Column(db.String(11))#最终绩效
    deduct_margin=db.Column(db.String(11))#本月保证金
    given_margin=db.Column(db.String(11))#返还总保证金
    deduct_payment=db.Column(db.String(11))#当月扣款
    total_payment=db.Column(db.String(11))#当月总工资

    def __init__(self,manager_id,manager_type,payment_time,position,base_payment,total_performance,
        assess_result,last_performance,deduct_margin,given_margin,deduct_payment,total_payment):
    	self.manager_id = manager_id
    	self.manager_type = manager_type
    	self.payment_time = payment_time
    	self.position = position
        self.base_payment = base_payment
        self.total_performance = total_performance
        self.assess_result = assess_result
        self.last_performance = last_performance
        self.deduct_margin = deduct_margin
        self.given_margin = given_margin
        self.deduct_payment = deduct_payment
        self.total_payment = total_payment


	def add(self):
		db.session.add(self)