#coding:utf-8
__author__ = 'Johnny'

from scapp import db

# 担保抵押调查表
class SC_Guarantee_mortgage(db.Model):
    '''
     担保抵押调查表
    '''
    __tablename__ = 'sc_guarantee_mortgage'
    id = db.Column(db.Integer, primary_key=True)
    loan_apply_id=db.Column(db.Integer)
    guarantee_remark=db.Column(db.VARCHAR(256))#共同借款人备注
    mortgage_remark=db.Column(db.VARCHAR(256))#担保人备注
    remark=db.Column(db.VARCHAR(256))#备注

    def __init__(self,loan_apply_id,guarantee_remark,mortgage_remark,remark):
        self.loan_apply_id = loan_apply_id
        self.guarantee_remark = guarantee_remark
        self.mortgage_remark = mortgage_remark
        self.remark = remark


    def add(self):
        db.session.add(self)