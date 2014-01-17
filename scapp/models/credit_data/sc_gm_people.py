#coding:utf-8
__author__ = 'Johnny'

from scapp import db

# 担保抵押调查表-担保人和共同借款人
class SC_GM_people(db.Model):
    '''
     担保抵押调查表-担保人和共同借款人
    '''
    __tablename__ = 'sc_gm_people'
    id = db.Column(db.Integer, primary_key=True)
    loan_apply_id=db.Column(db.Integer)
    type=db.Column(db.CHAR(1))#类型0:共同借款人1：担保人
    name=db.Column(db.VARCHAR(64))#姓名
    relationship=db.Column(db.VARCHAR(16))#与客户的关系
    id_num=db.Column(db.VARCHAR(32))#身份证号码
    home_tel=db.Column(db.VARCHAR(18))#家庭电话
    business_position=db.Column(db.VARCHAR(18))#主营业务或者职务
    address=db.Column(db.VARCHAR(128))#地址
    main_assets=db.Column(db.VARCHAR(64))#主要资产
    monthly_income=db.Column(db.Float(18,2))#月收入

    def __init__(self,loan_apply_id,name,relationship,id_num,home_tel,business_position,address,
                 main_assets,monthly_income):
        self.loan_apply_id = loan_apply_id
        self.name = name
        self.relationship = relationship
        self.id_num = id_num
        self.home_tel = home_tel
        self.business_position = business_position
        self.address = address
        self.main_assets = main_assets
        self.monthly_income = monthly_income


    def add(self):
        db.session.add(self)