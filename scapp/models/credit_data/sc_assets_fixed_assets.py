#coding:utf-8
__author__ = 'Johnny'

from scapp import db

# 资产负债表-固定资产
class SC_Assets_Fixed_Assets(db.Model):
    '''
    资产负债表-固定资产
    资产分类 0:房地产 1:设备 2:车辆
    '''
    __tablename__ = 'sc_assets_fixed_assets'
    id = db.Column(db.Integer, primary_key=True)
    loan_apply_id=db.Column(db.Integer)
    assets_type=db.Column(db.CHAR(1))#资产分类 0:房地产 1:设备 2:车辆
    assets_name=db.Column(db.String(128))#资产名称
    assets_ah=db.Column(db.String(16))#户主或数量
    describe=db.Column(db.String(16))#描述
    assets_date=db.Column(db.Date)#购置或建造时间
    price=db.Column(db.String(16))#购置价格
    amount=db.Column(db.String(16))#金额

    def __init__(self,loan_apply_id,assets_type,assets_name,assets_ah,describe,assets_date,price,amount):
    	self.loan_apply_id = loan_apply_id
    	self.assets_type = assets_type
    	self.assets_name = assets_name
    	self.assets_ah = assets_ah
    	self.describe = describe
    	self.assets_date = assets_date
    	self.price = price
    	self.amount = amount

	def add(self):
		db.session.add(self)