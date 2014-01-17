#coding:utf-8
__author__ = 'Johnny'

from scapp import db
import datetime
# 贷后变更记录表
class SC_change_record(db.Model):
    '''
    贷后变更记录表
    change_content:0:还款计划 1:修改担保人数据 2:修改共同借款人数据 3:修改抵押物信息
    '''
    __tablename__ = 'sc_change_record'
    id = db.Column(db.Integer, primary_key=True)
    loan_apply_id=db.Column(db.Integer)#贷款编号
    change_content=db.Column(db.Integer)#改变内容 0:还款计划 1:修改担保人数据 2:修改共同借款人数据 3:修改抵押物信息
    change_reason=db.Column(db.String(32))#变更原因
    change_describe=db.Column(db.String(256))#变更描述

    create_user = db.Column(db.Integer)
    create_date = db.Column(db.DateTime,default=datetime.datetime.now())


    def __init__(self,loan_apply_id,change_content,create_user,change_reason,change_describe):
    	self.loan_apply_id = loan_apply_id
    	self.change_content = change_content
        self.change_reason = change_reason
        self.change_describe = change_describe
        self.create_user=create_user


	def add(self):
		db.session.add(self)