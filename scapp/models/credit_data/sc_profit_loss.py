#coding:utf-8
from flask.ext.login import current_user

from scapp import db
import datetime

# 损益表
class SC_Profit_Loss(db.Model):
    '''
    损益表
    '''
    __tablename__ = 'sc_profit_loss'
    id = db.Column(db.Integer, primary_key=True)
    loan_apply_id=db.Column(db.Integer)
    items_name = db.Column(db.String(32))#名称
    items_type = db.Column(db.Integer)#类型
    index = db.Column(db.Integer) #同一类别序号
    month_1=db.Column(db.String(16))#月
    month_2=db.Column(db.String(16))#月
    month_3=db.Column(db.String(16))#月
    month_4=db.Column(db.String(16))#月
    month_5=db.Column(db.String(16))#月
    month_6=db.Column(db.String(16))#月
    month_7=db.Column(db.String(16))#月
    month_8=db.Column(db.String(16))#月
    month_9=db.Column(db.String(16))#月
    month_10=db.Column(db.String(16))#月
    month_11=db.Column(db.String(16))#月
    month_12=db.Column(db.String(16))#月
    total = db.Column(db.String(32))#总计
    pre_month = db.Column(db.String(32))#月平均

    create_user = db.Column(db.Integer)
    create_date = db.Column(db.DateTime)
    modify_user = db.Column(db.Integer)
    modify_date = db.Column(db.DateTime)

    def __init__(self,loan_apply_id,items_type,items_name,index,month_1,month_2,month_3,month_4,month_5,month_6,
        month_7,month_8,month_9,month_10,month_11,month_12,total,pre_month):
        self.loan_apply_id = loan_apply_id
        self.items_type = items_type
        self.items_name = items_name
        self.index = index
        self.month_1=month_1
        self.month_2=month_2
        self.month_3=month_3
        self.month_4=month_4
        self.month_5=month_5
        self.month_6=month_6
        self.month_7=month_7
        self.month_8=month_8
        self.month_9=month_9
        self.month_10=month_10
        self.month_11=month_11
        self.month_12=month_12
        self.total = total#总计
        self.pre_month = pre_month#月平均

        self.create_user = current_user.id
        self.create_date = datetime.datetime.now()

    def add(self):
        db.session.add(self)


