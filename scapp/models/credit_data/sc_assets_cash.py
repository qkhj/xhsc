#coding:utf-8
__author__ = 'Johnny'

from scapp import db

# 资产负债表-现金
class SC_Assets_cash(db.Model):
    '''
    资产负债表-现金
    '''
    __tablename__ = 'sc_assets_cash'
    id = db.Column(db.Integer, primary_key=True)
    loan_apply_id=db.Column(db.Integer)
    see_cash=db.Column(db.CHAR(1))#业务类型 0：未看到1：看到
    amount=db.Column(db.Float(18,2))#现金金额

    def __init__(self,loan_apply_id,see_cash,amount):
        self.loan_apply_id = loan_apply_id
        self.see_cash = see_cash
        self.amount = amount

    def add(self):
        db.session.add(self)