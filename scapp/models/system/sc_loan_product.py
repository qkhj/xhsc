# coding:utf-8
from scapp import db

class SC_Loan_Product(db.Model):
    __tablename__ = 'sc_loan_product'
    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String)#名称
    max_deadline = db.Column(db.Integer)#最高期限
    min_amount = db.Column(db.String)#最小金额
    max_amount = db.Column(db.String)#最大金额
    #product_type = db.Column(db.Integer, db.ForeignKey('sc_lp_type.id'))
    product_describe= db.Column(db.String)#描述

    #外键
    #pr_prtype = db.relationship('SC_LP_type', backref=db.backref('sc_loan_product',lazy='joined'))

    def __init__(self,product_name,max_deadline,min_amount,max_amount,product_describe):
        self.product_name = product_name
        self.max_deadline = max_deadline
        self.min_amount = min_amount
        self.max_amount = max_amount
        self.product_describe = product_describe

    def add(self):
        db.session.add(self)
