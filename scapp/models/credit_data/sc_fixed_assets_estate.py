#coding:utf-8
__author__ = 'Johnny'

from scapp import db

# 固定资产详单-房地产
class SC_Fixed_Assets_Estate(db.Model):
    '''
     固定资产详单-房地产
    '''
    __tablename__ = 'sc_fixed_assets_estate'
    id = db.Column(db.Integer, primary_key=True)
    loan_apply_id=db.Column(db.Integer)
    name=db.Column(db.String(32))#房地产名称
    # address=db.Column(db.String(64))#地址
    # gfa=db.Column(db.String(32))#建筑面积
    # land_area=db.Column(db.String(32))#土地面积
    # life= db.Column(db.String(32))#使用年限
    # land_type=db.Column(db.String(32))#土地性质--页面选择，后台直接填入中文
    purchase_price=db.Column(db.String(32))#购置价或造价
    # price=db.Column(db.String(32))#现价
    # remark=db.Column(db.String(64))#备注
    purchase_date=db.Column(db.Date)#购置时间
    total_price= db.Column(db.String(32))#总价
    rate =db.Column(db.Integer)#折旧率
    total =db.Column(db.Integer)#数量
    rate_price=db.Column(db.Integer)#折旧后价值
    

    def __init__(self,loan_apply_id,name,purchase_date,purchase_price,rate,total,total_price,
                 rate_price):
        self.loan_apply_id = loan_apply_id
        self.name = name
        self.purchase_date = purchase_date
        self.purchase_price = purchase_price
        self.total_price = total_price
        self.rate = rate
        self.total = total
        self.rate_price = rate_price


    def add(self):
        db.session.add(self)