#coding:utf-8
__author__ = 'Johnny'

from scapp import db

# 资产负债表-存款
class SC_Assets_Deposit(db.Model):
    '''
    资产负债表-存款
    '''
    __tablename__ = 'sc_assets_deposit'
    id = db.Column(db.Integer, primary_key=True)
    loan_apply_id=db.Column(db.Integer)
    bank=db.Column(db.String(64))#开户行
    account_type=db.Column(db.String(16))#账户类型
    account_no=db.Column(db.String(32))#帐号
    account_balance=db.Column(db.String(32))#余额

    def __init__(self,loan_apply_id,bank,account_type,account_no,account_balance):
        self.loan_apply_id = loan_apply_id
        self.bank = bank
        self.account_type = account_type
        self.account_no = account_no
        self.account_balance = account_balance

    def add(self):
        db.session.add(self)