#coding:utf-8
__author__ = 'Johnny'
from flask.ext.login import current_user
from scapp import db
import datetime
# 还款计划表
class SC_Repayment_Plan(db.Model):
    '''
    还款计划表
    '''
    __tablename__ = 'sc_repayment_plan'
    id = db.Column(db.Integer, primary_key=True)
    loan_apply_id=db.Column(db.Integer)#贷款编号
    repayment_type=db.Column(db.Integer)#还款方式 0:等额本息 1：等额本金 2：不等额还款
    amount=db.Column(db.DECIMAL(18,2))#还款总额
    first_repayment_date=db.Column(db.DateTime)#第一次还款时间
    lending_date=db.Column(db.DateTime)#贷款发放日期
    ratio=db.Column(db.DECIMAL(6,2))#利率
    installmenst=db.Column(db.Integer)#期数

    create_user=db.Column(db.Integer)
    create_date=db.Column(db.DateTime,default=datetime.datetime.now())#创建日期
    modify_user=db.Column(db.Integer)
    modify_date=db.Column(db.DateTime,default=datetime.datetime.now())#修改日期

    def __init__(self,loan_apply_id,repayment_type,
                 amount,first_repayment_date,lending_date,ratio,installmenst):
    	self.loan_apply_id = loan_apply_id
        self.repayment_type = repayment_type
    	self.amount = amount
    	self.first_repayment_date = first_repayment_date
    	self.lending_date = lending_date
    	self.ratio = ratio
        self.installmenst = installmenst
        self.create_user = current_user.id
    	self.create_date = datetime.datetime.now()
    	self.modify_user = current_user.id
    	self.modify_date = datetime.datetime.now()

    def add(self):
    	db.session.add(self)