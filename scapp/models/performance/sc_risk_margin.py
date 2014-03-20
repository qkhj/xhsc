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
    manager_id=db.Column(db.String(11))#员工工号
    manager_type=db.Column(db.String(11))#员工类型
    given_margin=db.Column(db.String(11))#返还总保证金
    overduce_margin=db.Column(db.String(11))#逾期保证金
    total_margin=db.Column(db.String(11))#总保证金

    def __init__(self,manager_id,manager_type,given_margin,overduce_margin,total_margin):
    	self.manager_id = manager_id
    	self.manager_type = manager_type
    	self.given_margin = given_margin
    	self.overduce_margin = overduce_margin
        self.total_margin = total_margin

	def add(self):
		db.session.add(self)