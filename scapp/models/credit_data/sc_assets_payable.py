#coding:utf-8
__author__ = 'Johnny'

from scapp import db

# 资产负债表-应付账款
class SC_Assets_payable(db.Model):
    '''
    资产负债表-应付账款
    应付账款类型 0:应付供货商1：其它应付账款
    '''
    __tablename__ = 'sc_assets_payable'
    id = db.Column(db.Integer, primary_key=True)
    loan_apply_id=db.Column(db.Integer)
    payable_type=db.Column(db.CHAR(1))#应付账款类型 0:应付供货商1：其它应付账款
    customer_name=db.Column(db.VARCHAR(64))#应付对象
    describe=db.Column(db.VARCHAR(32))#描述
    amount=db.Column(db.Float(18,2))#金额

    def __init__(self,loan_apply_id,payable_type,customer_name,describe,amount):
        self.loan_apply_id = loan_apply_id
        self.payable_type = payable_type
        self.customer_name = customer_name
        self.describe = describe
        self.amount = amount

    def add(self):
        db.session.add(self)