# coding:utf-8
__author__ = 'johhny'

# coding:utf-8
"""
    scapp.system.sc_lp_type
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    贷款产品类型模型
"""
__author__ = 'johhny'

from scapp import db

class SC_LP_Type(db.Model):
    __tablename__ = 'sc_loan_product'
    id = db.Column(db.Integer, primary_key=True)
    type_name = db.Column(db.String)

    def __init__(self,type_name):
        self.type_name = type_name


    def add(self):
        db.session.add(self)
