#coding:utf-8
__author__ = 'Johnny'

from scapp import db
import datetime
# 每期还款记录表
class SC_Repayment(db.Model):
    '''
    每期还款记录表
    还款状态status：0：未还，1：已还未还清，2：逾期未还 3:还清
    '''
    __tablename__ = 'sc_repayment'
    id = db.Column(db.Integer, primary_key=True)
    repayment_plan_detail_id=db.Column(db.Integer)#还款计划主键
    loan_apply_id=db.Column(db.Integer)#贷款编号
    # customer_no=db.Column(db.String(32))#客户号
    # contract_no=db.Column(db.String(32))#合同号
    # account=db.Column(db.String(32))#账号
    repayment_installments=db.Column(db.Integer,autoincrement=True)#当前还款期数
    clear_date=db.Column(db.DateTime)#实际还款日期
    re_principal=db.Column(db.DECIMAL(18,2))#当期本金剩余
    re_interest=db.Column(db.DECIMAL(18,2))#当期利息剩余
    re_interest_balance=db.Column(db.DECIMAL(18,2))#当期罚息剩余
    principal_fx_balance=db.Column(db.DECIMAL(18,2))#本金罚息剩余
    interest_fx_balance=db.Column(db.DECIMAL(18,2))#利息罚息剩余
    total_fx=db.Column(db.DECIMAL(18,2))#当期实际缴纳罚息总额
    total_repayment=db.Column(db.DECIMAL(18,2))#当期实际还款总额
    status=db.Column(db.Integer)#当前状态 0：未还，1：已还未还清，2：逾期未还 3:还清
    repayment_clear_date=db.Column(db.DateTime)#本期借款实际结清日期
    modify_date=db.Column(db.DateTime,default=datetime.datetime.now())#修改日期

    def __init__(self,repayment_plan_detail_id,loan_apply_id,customer_no,
                 contract_no,account,repayment_installments,clear_date,re_principal,re_interest,
                 re_interest_balance,principal_fx_balance,interest_fx_balance,total_fx,total_repayment,
                 status,repayment_clear_date):
    	self.repayment_plan_detail_id = repayment_plan_detail_id
    	self.loan_apply_id = loan_apply_id
    	# self.customer_no = customer_no
    	# self.contract_no = contract_no
    	# self.account = account
    	self.repayment_installments = repayment_installments
        self.clear_date = clear_date
    	self.re_principal = re_principal
    	self.re_interest = re_interest
    	self.re_interest_balance = re_interest_balance
    	self.principal_fx_balance = principal_fx_balance
    	self.interest_fx_balance = interest_fx_balance
        self.total_fx = total_fx
    	self.total_repayment = total_repayment
    	self.status = status
    	self.repayment_clear_date = repayment_clear_date
        self.modify_date = datetime.datetime.now()

    def add(self):
    	db.session.add(self)