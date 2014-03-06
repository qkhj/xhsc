#coding:utf-8
__author__ = 'Johnny'

from scapp import db

# 账款清单
class SC_Accounts_List(db.Model):
    '''
     账款清单
    '''
    __tablename__ = 'sc_accounts_list'
    id = db.Column(db.Integer, primary_key=True)
    loan_apply_id=db.Column(db.Integer)
    name=db.Column(db.String(32))#对象名称
    original_price= db.Column(db.String(32))#原始金额
    occur_date=db.Column(db.Date)#发生日期
    deadline=db.Column(db.Date)#到期日
    present_price= db.Column(db.String(32))#现值
    cooperation_history=db.Column(db.String(32))#合作历史
    # average_period=db.Column(db.String(32))#平均帐期
    # trading_frequency=db.Column(db.String(32)) #交易频率--页面选择，后台直接填入中文
    # turnover= db.Column(db.String(32))#分析期内的交易额
    pay_type=db.Column(db.String(32)) #支付方式--页面选择，后台直接填入中文
    # source=db.Column(db.String(32)) #信息来源--页面选择，后台直接填入中文
    # other_info=db.Column(db.String(64)) #其他信息
    mode_type = db.Column(db.Integer)#1-应付，2-应收

    def __init__(self,loan_apply_id,name,original_price,occur_date,deadline,present_price,cooperation_history,pay_type,mode_type):
        self.loan_apply_id = loan_apply_id
        self.name = name
        self.original_price = original_price
        self.occur_date = occur_date
        self.deadline = deadline
        self.present_price = present_price
        self.cooperation_history = cooperation_history
        self.pay_type = pay_type
        self.mode_type = mode_type
    def add(self):
        db.session.add(self)