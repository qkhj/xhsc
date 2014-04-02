#coding:utf-8
__author__ = 'hejia'

from scapp import db
import datetime

class SC_risk_margin(db.Model):
    '''
    风险保证金
    '''
    __tablename__ = 'sc_risk_margin'
    id = db.Column(db.Integer, primary_key=True)
    manager_id=db.Column(db.Integer,db.ForeignKey('sc_user.id'))#员工工号
    given_margin=db.Column(db.String(11))#返还总保证金
    overduce_margin=db.Column(db.String(11))#逾期保证金
    dedcut_margin=db.Column(db.String(11))#扣除保证金
    total_margin=db.Column(db.String(11))#总保证金

    # 外键名称
    risk_margin_fk = db.relationship('SC_User',foreign_keys=[manager_id], backref = db.backref('risk_margin_fk', lazy = 'dynamic'))
    def __init__(self,manager_id,given_margin,overduce_margin,dedcut_margin,total_margin):
    	self.manager_id = manager_id
    	self.given_margin = given_margin
    	self.overduce_margin = overduce_margin
        self.dedcut_margin = dedcut_margin
        self.total_margin = total_margin

	def add(self):
		db.session.add(self)