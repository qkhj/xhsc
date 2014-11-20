# coding:utf-8
from scapp import db
from flask.ext.login import current_user

#客户经理本地数据表
class SC_Local_Excel(db.Model):
	__tablename__ = 'sc_local_excel'
	id=db.Column(db.Integer, primary_key=True)
	user_id=db.Column(db.Integer)
	attachment=db.Column(db.String(255))
	is_sync=db.Column(db.Integer)

	def __init__(self,user_id,attachment):
		self.user_id = user_id
		self.attachment = attachment

	def add(self):
		db.session.add(self)

  
