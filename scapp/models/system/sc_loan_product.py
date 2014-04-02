# coding:utf-8
"""
    scapp.system.sc_loan_product
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    贷款产品模型
"""
__author__ = 'johhny'

from scapp import db

class SC_Loan_Product(db.Model):
    __tablename__ = 'sc_loan_product'
    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String)
    product_type = db.Column(db.Integer, db.ForeignKey('sc_lp_type.id'))
    product_describe= db.Column(db.String)


    #外键
    pr_prtype = db.relationship('SC_LP_type', backref=db.backref('sc_loan_product',lazy='joined'))

    def __init__(self,product_name,product_type,product_describe):
        self.product_name = product_name
        self.product_type = product_type
        self.product_describe = product_describe


    def add(self):
        db.session.add(self)
