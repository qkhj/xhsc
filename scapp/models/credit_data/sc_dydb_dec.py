#coding:utf-8
from scapp import db
#现金流子表费用信息汇总表
class SC_Dydb_Dec(db.Model):
    __tablename__ = 'sc_dydb_dec'
    id = db.Column(db.Integer, primary_key=True)
    loan_apply_id=db.Column(db.Integer)
    dec = db.Column(db.String)

    def __init__(self,loan_apply_id,dec):
        self.loan_apply_id = loan_apply_id
        self.dec = dec

    def add(self):
        db.session.add(self)