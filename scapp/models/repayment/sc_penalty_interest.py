#coding:utf-8
__author__ = 'Johnny'

from scapp import db
import datetime
# 罚息记录
class SC_Penalty_Interest(db.Model):
    '''
    罚息记录表
    '''
    __tablename__ = 'sc_penalty_interest'
    id = db.Column(db.Integer, primary_key=True)
    repayment_id=db.Column(db.Integer)#还款主键
    amount=db.Column(db.DECIMAL(18,2))#罚息金额
    principal_amount=db.Column(db.DECIMAL(18,2))#本罚
    interest_amount=db.Column(db.DECIMAL(18,2))#利罚
    principal_base=db.Column(db.DECIMAL(18,2))#罚息时本金基数
    interest_base=db.Column(db.DECIMAL(18,2))#罚息时利息基数
    penalty_date=db.Column(db.DateTime)#罚息日期
    create_date=db.Column(db.DateTime,default=datetime.datetime.now())#创建日期
    modify_date=db.Column(db.DateTime)#修改日期

    def __init__(self,repayment_id,amount,principal_amount,interest_amount,principal_base,interest_base,penalty_date):
    	self.repayment_id = repayment_id
    	self.amount = amount
    	self.principal_amount = principal_amount
    	self.interest_amount = interest_amount
    	self.principal_base = principal_base
    	self.interest_base = interest_base
    	self.penalty_date = penalty_date
        self.modify_date = datetime.datetime.now()


	def add(self):
		db.session.add(self)