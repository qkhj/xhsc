#coding:utf-8
__author__ = 'Johnny'

from scapp import db

# 资产负债表-承兑汇票
class SC_Assets_Acceptances(db.Model):
    '''
    资产负债表-承兑汇票
    '''
    __tablename__ = 'sc_assets_acceptances'
    id = db.Column(db.Integer, primary_key=True)
    loan_apply_id=db.Column(db.Integer)
    bank=db.Column(db.String(64))#出票行
    account_expiry_date=db.Column(db.Date)#到期日
    account_balance=db.Column(db.String(32))#余额

    def __init__(self,loan_apply_id,bank,account_expiry_date,account_balance):
        self.loan_apply_id = loan_apply_id
        self.bank = bank
        self.account_expiry_date = account_expiry_date
        self.account_balance = account_balance

    def add(self):
        db.session.add(self)