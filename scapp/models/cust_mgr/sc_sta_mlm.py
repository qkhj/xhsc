# coding:utf-8
"""
    scapp.cust_mgr.sc_sta_mlm
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    客户经理贷款情况统计模型
"""
__author__ = 'johhny'

from scapp import db

class SC_Sta_Mlm(db.Model):
    __tablename__ = 'sc_sta_mlm'
    id = db.Column(db.Integer, primary_key=True)
    user_id =db.Column(db.Integer, db.ForeignKey('sc_user.id')) #用户ID
    intrest=db.Column(db.Float) #当月利润贡献
    defact_rate=db.Column(db.Float) #当月瑕疵贷款率
    overdue_rate=db.Column(db.Float) #当月当前逾期率
    overdue_amount=db.Column(db.Float) #当月当前逾期金额
    month=db.Column(db.Integer) #当前月份


    #外键
    sta_user = db.relationship('SC_User', backref=db.backref('sc_sta_mlm',lazy='joined'))

    def __init__(self,user_id,intrest,defact_rate,overdue_rate,overdue_amount,month):
        self.user_id = user_id
        self.intrest = intrest
        self.defact_rate = defact_rate
        self.overdue_rate = overdue_rate
        self.overdue_amount = overdue_amount
        self.month = month

    def add(self):
        db.session.add(self)
