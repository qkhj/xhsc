#coding:utf-8
__author__ = 'hejia'

from scapp import db
import datetime

class SC_assess_record(db.Model):
    '''
    评估记录表
    '''
    __tablename__ = 'sc_assess_record'
    id = db.Column(db.Integer, primary_key=True)
    manager_id=db.Column(db.Integer)#员工工号
    assess_time=db.Column(db.String(11))#评估时间
    assess_arg=db.Column(db.String(11))#最近三次评估平均分
    assess_sum=db.Column(db.String(11))#评估次数
    assess_score_1=db.Column(db.String(11))#最近的一次评估分
    assess_score_2=db.Column(db.String(11))#最近的两次评估分
    assess_score_3=db.Column(db.String(11))#最近的三次评估分

    def __init__(self,manager_id):
    	self.manager_id = manager_id

    def add(self):
    	db.session.add(self)