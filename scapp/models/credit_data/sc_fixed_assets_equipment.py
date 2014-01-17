#coding:utf-8
__author__ = 'Johnny'

from scapp import db

# 固定资产详单-设备或器材
class SC_Fixed_Assets_Equipment(db.Model):
    '''
     固定资产详单-设备或器材
    '''
    __tablename__ = 'sc_fixed_assets_equipment'
    id = db.Column(db.Integer, primary_key=True)
    loan_apply_id=db.Column(db.Integer)
    name=db.Column(db.String(32))#设备名称
    amount=db.Column(db.Integer)#数量
    type_brand=db.Column(db.String(32))#型号或品牌
    purchase_date=db.Column(db.Date)#购置时间
    production_date=db.Column(db.Date)#生产时间
    total_price= db.Column(db.String(32))#总价
    outward=db.Column(db.String(64))#外观评价
    remark=db.Column(db.String(64))#备注


    def __init__(self,loan_apply_id,name,amount,type_brand,purchase_date,production_date,total_price,
                 outward,remark):
        self.loan_apply_id = loan_apply_id
        self.name = name
        self.amount = amount
        self.type_brand = type_brand
        self.purchase_date = purchase_date
        self.production_date = production_date
        self.total_price = total_price
        self.outward = outward
        self.remark = remark


    def add(self):
        db.session.add(self)