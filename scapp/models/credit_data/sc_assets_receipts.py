#coding:utf-8
__author__ = 'Johnny'

from scapp import db

# 资产负债表-预收账款
class SC_Assets_receipts(db.Model):
    '''
    资产负债表-预收账款
    '''
    __tablename__ = 'sc_assets_receipts'
    id = db.Column(db.Integer, primary_key=True)
    loan_apply_id=db.Column(db.Integer)
    source=db.Column(db.VARCHAR(32))#预收来源
    occur_date=db.Column(db.DateTime)#发生日期
    describe=db.Column(db.VARCHAR(16))#描述
    amount=db.Column(db.Float(18,2))#金额

    def __init__(self,loan_apply_id,source,occur_date,describe,amount):
        self.loan_apply_id = loan_apply_id
        self.source = source
        self.occur_date = occur_date
        self.describe = describe
        self.amount = amount

    def add(self):
        db.session.add(self)