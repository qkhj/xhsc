#coding:utf-8
__author__ = 'Johnny'

from scapp import db

# 担保抵押调查表-抵押物
class SC_GM_good(db.Model):
    '''
     担保抵押调查表-抵押物
    '''
    __tablename__ = 'sc_gm_good'
    id = db.Column(db.Integer, primary_key=True)
    loan_apply_id=db.Column(db.Integer)
    name=db.Column(db.VARCHAR(64))#物品名称
    owner_address=db.Column(db.VARCHAR(64))#所有者或地址
    describe=db.Column(db.VARCHAR(64))#描述
    registration_number=db.Column(db.VARCHAR(32))#登记号
    appraisal=db.Column(db.Float(18,2))#估价
    mortgage=db.Column(db.Float(18,2))#抵押
    pledge=db.Column(db.CHAR(1))#质押 0:是 1：否

    def __init__(self,loan_apply_id,name,owner_address,describe,registration_number,appraisal,mortgage,
                 pledge):
        self.loan_apply_id = loan_apply_id
        self.name = name
        self.owner_address = owner_address
        self.describe = describe
        self.registration_number = registration_number
        self.appraisal = appraisal
        self.mortgage = mortgage
        self.pledge = pledge


    def add(self):
        db.session.add(self)