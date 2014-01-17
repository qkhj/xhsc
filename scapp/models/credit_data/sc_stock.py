#coding:utf-8
__author__ = 'Johnny'

from scapp import db

# 库存
class SC_Stock(db.Model):
    '''
     库存
    '''
    __tablename__ = 'sc_stock'
    id = db.Column(db.Integer, primary_key=True)
    loan_apply_id=db.Column(db.Integer)
    name=db.Column(db.String(32))#货物名称
    amount=db.Column(db.String(32))#数量
    purchase_price=db.Column(db.String(32))#买进单价
    purchase_total_price=db.Column(db.String(32))#买进总价格
    sell_price=db.Column(db.String(32))#卖出价格
    sell_total_price=db.Column(db.String(32))#卖出总价格
    pre_rate=db.Column(db.String(32))#毛利率


    def __init__(self,loan_apply_id,name,amount,purchase_price,purchase_total_price,
        sell_price,sell_total_price,pre_rate):
        self.loan_apply_id = loan_apply_id
        self.name = name
        self.amount = amount
        self.purchase_price = purchase_price
        self.purchase_total_price = purchase_total_price
        self.sell_price = sell_price
        self.sell_total_price = sell_total_price
        self.pre_rate=pre_rate


    def add(self):
        db.session.add(self)