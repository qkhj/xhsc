#coding:utf-8
__author__ = 'Johnny'

from scapp import db
import datetime
# 还款计划详细表
class SC_Repayment_plan_detail(db.Model):
    '''
    还款计划详细表
    '''
    __tablename__ = 'sc_repayment_plan_detail'
    id = db.Column(db.Integer, primary_key=True)
    repayment_plan_id=db.Column(db.Integer)#还款计划主键
    loan_apply_id=db.Column(db.Integer)#贷款编号
    loan_balance=db.Column(db.DECIMAL(18,2))#当期的贷款余额
    termily_ratio=db.Column(db.DECIMAL(18,2))#当期利率
    principal=db.Column(db.DECIMAL(18,2))#本期本金
    interest=db.Column(db.DECIMAL(18,2))#本期利息
    total=db.Column(db.DECIMAL(18,2))#本期计划还款总额
    repayment_installments=db.Column(db.Integer,autoincrement=True)#还款期数
    clear_date=db.Column(db.DateTime)#还款日
    days=db.Column(db.Integer)#与上次还款间隔天数
    change_record=db.Column(db.Integer)#还款计划改变记录，每次新增取当前数据最大值然后+1
    modify_date=db.Column(db.DateTime,default=datetime.datetime.now())#修改日期

    def __init__(self,repayment_plan_id,loan_apply_id,loan_balance,
                 termily_ratio,principal,interest,total,repayment_installments,clear_date,
                 days,change_record):
    	self.repayment_plan_id = repayment_plan_id
    	self.loan_apply_id = loan_apply_id
    	self.loan_balance = loan_balance
        self.termily_ratio = termily_ratio
    	self.principal = principal
    	self.interest = interest
    	self.total = total
    	self.repayment_installments = repayment_installments
    	self.clear_date = clear_date
        self.days = days
        self.change_record=change_record
        self.modify_date = datetime.datetime.now()

    def add(self):
    	db.session.add(self)