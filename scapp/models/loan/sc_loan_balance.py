#coding:utf-8
__author__ = 'Johnny'

from scapp import db
import datetime
# 剩余贷款记录表
class SC_Loan_balance(db.Model):
    '''
    剩余贷款记录表
    '''
    __tablename__ = 'sc_loan_balance'
    id = db.Column(db.Integer, primary_key=True)
    loan_apply_id=db.Column(db.Integer)#贷款编号
    loan_amount=db.Column(db.DECIMAL(18,2))#申请金额
    loan_balance=db.Column(db.DECIMAL(18,2))#剩余本金
    loan_cleared_amount=db.Column(db.DECIMAL(18,2))#已还金额
    loan_interest_total=db.Column(db.DECIMAL(18,2))#利息总计
    loan_cleared_interest=db.Column(db.DECIMAL(18,2))#已还利息
    over_due_principal=db.Column(db.DECIMAL(18,2))#逾期本金
    over_due_interest=db.Column(db.DECIMAL(18,2))#逾期利息
    over_due_days=db.Column(db.Integer)#逾期天数
    cleard_pi=db.Column(db.DECIMAL(18,2))#收到的罚息
    modify_date=db.Column(db.DateTime,default=datetime.datetime.now())#修改日期


    def __init__(self,loan_apply_id,loan_amount,
                 loan_balance,loan_cleared_amount,loan_interest_total,loan_cleared_interest,over_due_principal,
                 over_due_interest,over_due_days,cleard_pi):
    	self.loan_apply_id = loan_apply_id
    	self.loan_amount = loan_amount
    	self.loan_balance = loan_balance
    	self.loan_cleared_amount = loan_cleared_amount
    	self.loan_interest_total = loan_interest_total
        self.loan_cleared_interest = loan_cleared_interest
    	self.over_due_principal = over_due_principal
    	self.over_due_interest = over_due_interest
    	self.over_due_days = over_due_days
    	self.cleard_pi = cleard_pi
        self.modify_date = datetime.datetime.now()


	def add(self):
		db.session.add(self)