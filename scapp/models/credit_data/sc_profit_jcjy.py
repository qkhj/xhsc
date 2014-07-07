#coding:utf-8
from scapp import db

# 毛利润交叉检验
class SC_Profit_Jcjy(db.Model):
    __tablename__ = 'sc_profit_jcjy'
    id=db.Column(db.Integer, primary_key=True)
    loan_apply_id=db.Column(db.Integer)
    type = db.Column(db.Integer) #类别
    index = db.Column(db.Integer) #递增的序号 从0开始
    name = db.Column(db.String) #名称
    bid = db.Column(db.String) #进价
    price = db.Column(db.String) #售价
    ratio = db.Column(db.String) #占比
    profit = db.Column(db.String) #毛利

    def __init__(self,loan_apply_id, type, index,name, bid,price,ratio,profit):
        self.loan_apply_id = loan_apply_id
        self.type = type
        self.index = index
        self.name = name
        self.bid = bid
        self.price = price
        self.ratio = ratio
        self.profit = profit

    def add(self):
        db.session.add(self)