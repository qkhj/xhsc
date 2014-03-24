#coding:utf-8
__author__ = 'hejia'

from scapp import db
import datetime

class SC_loan_income_list(db.Model):
    '''
    薪酬详单表
    '''
    __tablename__ = 'sc_loan_income_list'
    id = db.Column(db.Integer, primary_key=True)
    loan_apply_id=db.Column(db.String(11))#贷款编号
    loan_goal=db.Column(db.String(11))#贷款金额
    loan_rest=db.Column(db.String(11))#贷款利息
    singel_performance=db.Column(db.String(11))#所得绩效
    month_payment=db.Column(db.String(11))#当月收入
    manager_id=db.Column(db.String(11))#员工工号
    create_time=db.Column(db.String(11))#记录时间
    level_id=db.Column(db.String(11))#级别

    def __init__(self,loan_apply_id,loan_goal,loan_rest,singel_performance,month_payment,manager_id,create_time
        ,level_id):
    	self.loan_apply_id = loan_apply_id
    	self.loan_goal = loan_goal
    	self.loan_rest = loan_rest
    	self.singel_performance = singel_performance
        self.month_payment = month_payment
        self.manager_id = manager_id
        self.create_time = create_time
        self.level_id = level_id

	def add(self):
		db.session.add(self)