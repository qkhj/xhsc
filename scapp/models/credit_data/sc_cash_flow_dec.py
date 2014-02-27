#coding:utf-8
from scapp import db
#现金流子表费用信息汇总表
class SC_Cash_Flow_Dec(db.Model):
    __tablename__ = 'sc_cash_flow_dec'
    id = db.Column(db.Integer, primary_key=True)
    loan_apply_id=db.Column(db.Integer)
    dec_1 = db.Column(db.String)
    dec_2 = db.Column(db.String)

    def __init__(self,loan_apply_id,dec_1,dec_2):
        self.loan_apply_id = loan_apply_id
        self.dec_1 = dec_1
        self.dec_2 = dec_2

    def add(self):
        db.session.add(self)