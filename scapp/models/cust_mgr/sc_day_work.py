# coding:utf-8
__author__ = 'johhny'


from scapp import db
from flask.ext.login import current_user

import datetime

# 客户经理工作记录
class SC_Day_Work(db.Model):
    '''
     客户经理工作记录
    '''
    __tablename__ = 'sc_day_work'
    id = db.Column(db.Integer, primary_key=True)
    work_type=db.Column(db.String(32))#工作内容
    work_type_detail=db.Column(db.String(32))#工作内容子项
    beg_date=db.Column(db.DateTime)#开始时间
    end_date=db.Column(db.DateTime)#结束时间
    time_consume=db.Column(db.DECIMAL(5,2))#耗时
    remark=db.Column(db.String(256))

    create_user = db.Column(db.Integer,db.ForeignKey('sc_user.id'))
    create_date = db.Column(db.DateTime)
    modify_user = db.Column(db.Integer)
    modify_date = db.Column(db.DateTime)

    def __init__(self,work_type,work_type_detail,beg_date,end_date,time_consume,remark):
        self.work_type = work_type
        self.work_type_detail = work_type_detail
        self.beg_date = beg_date
        self.end_date = end_date
        self.time_consume=time_consume
        self.remark=remark
        self.create_user = current_user.id
        self.create_date = datetime.datetime.now()
        self.modify_user = current_user.id
        self.modify_date = datetime.datetime.now()

     # 外键名称
    receiver_for_sdw = db.relationship('SC_User',foreign_keys=[create_user], backref = db.backref('receiver_for_sdw', lazy = 'dynamic'))

    def add(self):
        db.session.add(self)

