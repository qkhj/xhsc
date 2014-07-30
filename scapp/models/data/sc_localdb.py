# coding:utf-8
from scapp import db
from flask.ext.login import current_user

#客户经理本地数据表
class SC_LocalDB(db.Model):
	__tablename__ = 'sc_localdb'
	id=db.Column(db.Integer, primary_key=True)
	user_id=db.Column(db.Integer)
	attachment=db.Column(db.String(255))

	def __init__(self,user_id,attachment):
		self.user_id = user_id
		self.attachment = attachment

	def add(self):
		db.session.add(self)

  
