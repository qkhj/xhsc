#coding:utf-8
__author__ = 'Johnny'

from scapp import db

# 固定资产详单-车辆
class SC_Fixed_Assets_Car(db.Model):
    '''
     固定资产详单-车辆
    '''
    __tablename__ = 'sc_fixed_assets_car'
    id = db.Column(db.Integer, primary_key=True)
    loan_apply_id=db.Column(db.Integer)
    name=db.Column(db.String(32))#车辆名称
    owner=db.Column(db.String(32))#持有人
    type_brand=db.Column(db.String(32))#型号或品牌
    purchase_date=db.Column(db.Date)#购置时间
    purchase_price=db.Column(db.String(32))#购置价格
    production_date=db.Column(db.Date)#生产时间
    total_price= db.Column(db.String(32))#总价
    outward=db.Column(db.String(64))#外观评价
    remark=db.Column(db.String(64))#备注


    def __init__(self,loan_apply_id,name,owner,type_brand,purchase_date,purchase_price,production_date,total_price,
                 outward,remark):
        self.loan_apply_id = loan_apply_id
        self.name = name
        self.owner = owner
        self.type_brand = type_brand
        self.purchase_date = purchase_date
        self.purchase_price = purchase_price
        self.production_date = production_date
        self.total_price = total_price
        self.outward = outward
        self.remark = remark


    def add(self):
        db.session.add(self)