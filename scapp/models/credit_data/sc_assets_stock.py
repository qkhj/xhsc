#coding:utf-8
__author__ = 'Johnny'

from scapp import db

# 资产负债表-存货
class SC_Assets_Stock(db.Model):
    '''
    资产负债表-存货
    '''
    __tablename__ = 'sc_assets_stock'
    id = db.Column(db.Integer, primary_key=True)
    loan_apply_id=db.Column(db.Integer)
    stock_type=db.Column(db.String(16))#存货分类
    stock_evaluate=db.Column(db.String(64))#存货外观质量评价
    stock_mobility=db.Column(db.String(16))#存货流动性
    proportion=db.Column(db.String(16))#比例
    amount=db.Column(db.String(16))#金额

    def __init__(self,loan_apply_id,stock_type,stock_evaluate,stock_mobility,proportion,amount):
        self.loan_apply_id = loan_apply_id
        self.stock_type = stock_type
        self.stock_evaluate = stock_evaluate
        self.stock_mobility = stock_mobility
        self.proportion = proportion
        self.amount = amount

    def add(self):
        db.session.add(self)