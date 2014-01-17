#coding:utf-8
__author__ = 'Johnny'
from scapp import db
#现金流子表费用信息汇总表
class SC_Cash_Flow_Assist(db.Model):
    '''
    现金流子表费用信息汇总表
    数据类型 0：其它费用信息 1：其它借款 2：偿还其它借款 3：其它借款现金来源
             #损益表中-4:经营收入 5：可变成本6：其他
    '''
    __tablename__ = 'sc_cash_flow_assist'
    id = db.Column(db.Integer, primary_key=True)
    loan_apply_id=db.Column(db.Integer)
    type=db.Column(db.CHAR(1))#业务类型 0：业务历史1：业务展望
    assist_type=db.Column(db.CHAR(1))#数据类型 0：其它费用信息 1：其它借款 2：偿还其它借款 3：其它借款现金来源
                                    #损益表中-4:经营收入 5：可变成本6：其他
    name=db.Column(db.String(32))#费用名称
    month_0=db.Column(db.String(16))#月数
    month_1=db.Column(db.String(16))
    month_2 = db.Column(db.String(16))
    month_3 = db.Column(db.String(16))
    month_4 = db.Column(db.String(16))
    month_5 = db.Column(db.String(16))
    month_6 = db.Column(db.String(16))
    month_7= db.Column(db.String(16))
    month_8 = db.Column(db.String(16))
    month_9 = db.Column(db.String(16))
    month_10 = db.Column(db.String(16))
    month_11 = db.Column(db.String(16))
    month_12 = db.Column(db.String(16))


    def __init__(self,loan_apply_id,type,assist_type,name,month_0,
                 month_1,month_2,month_3,month_4,month_5,
                 month_6,month_7,month_8,month_9,month_10,month_11,month_12):
        self.loan_apply_id = loan_apply_id
        self.type = type
        self.assist_type = assist_type
        self.name = name
        self.month_0 = month_0
        self.month_1 = month_1
        self.month_2 = month_2
        self.month_3 = month_3
        self.month_4 = month_4
        self.month_5 = month_5
        self.month_6 = month_6
        self.month_7 = month_7
        self.month_8 = month_8
        self.month_9 = month_9
        self.month_10 = month_10
        self.month_11 = month_11
        self.month_12 = month_12



    def add(self):
        db.session.add(self)