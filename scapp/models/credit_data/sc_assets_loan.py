#coding:utf-8
__author__ = 'Johnny'

from scapp import db


class SC_Assets_loan(db.Model):
    '''
    资产负债表-借款，集资，负债
    loan_type:0：短期银行借款1：短期社会集资2：长期银行借款3：长期社会集资4：其它表外负债
    '''
    __tablename__ = 'sc_assets_loan'
    id = db.Column(db.Integer, primary_key=True)
    loan_apply_id=db.Column(db.Integer)
    loan_type=db.Column(db.CHAR(1))#贷款类型 0：短期银行借款1：短期社会集资2：长期银行借款3：长期社会集资4：其它表外负债
    loan_org=db.Column(db.VARCHAR(32))#贷款机构
    loan_amount=db.Column(db.Float(18,2))#贷款金额
    loan_date=db.Column(db.DateTime)#放款日期
    loan_deadline=db.Column(db.Integer)#期限
    guarantee=db.Column(db.VARCHAR(16))#担保方式/与借款人关系
    banlance=db.Column(db.Float(18,2))#贷款余额/金额

    def __init__(self,loan_apply_id,loan_type,loan_org,loan_amount,loan_date,loan_deadline,guarantee,banlance):
        self.loan_apply_id = loan_apply_id
        self.loan_type = loan_type
        self.loan_org = loan_org
        self.loan_amount = loan_amount
        self.loan_date = loan_date
        self.loan_deadline = loan_deadline
        self.guarantee = guarantee
        self.banlance = banlance


    def add(self):
        db.session.add(self)