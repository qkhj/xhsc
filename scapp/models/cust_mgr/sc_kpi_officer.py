# coding:utf-8
from scapp import db
from flask.ext.login import current_user

#在岗考核表-客户经理
class SC_Kpi_Officer(db.Model):
	__tablename__ = 'sc_kpi_officer'
	id = db.Column(db.Integer, primary_key=True)
	officer_level = db.Column(db.Integer)
	assess_date = db.Column(db.Date)
	bq_dkye = db.Column(db.String(4))
	bq_ghs = db.Column(db.String(4))
	bq_khs = db.Column(db.String(4))
	bq_lxsr = db.Column(db.String(4))
	bq_zsbs = db.Column(db.String(4))
	bm_dkye = db.Column(db.String(4))
	bm_ghs = db.Column(db.String(4))
	bm_lrgxd = db.Column(db.String(4))
	gr_dkye = db.Column(db.String(4))
	gr_ghs = db.Column(db.String(4))
	gr_xzkhs = db.Column(db.String(4))
	gr_zsbs = db.Column(db.String(4))
	gr_lrgxd = db.Column(db.String(4))
	rcxwpg = db.Column(db.String(4))
	yql = db.Column(db.String(16))
	total = db.Column(db.String(4))
	result = db.Column(db.Integer)
	qtpj = db.Column(db.String(255))
	xq_dkye = db.Column(db.String(16))
	xq_ghs = db.Column(db.String(16))
	xq_xzkhs = db.Column(db.String(16))
	xq_lxsr = db.Column(db.String(16))
	xq_zsbs = db.Column(db.String(16))
	user_id = db.Column(db.Integer, db.ForeignKey('sc_user.id'))
	Date_1 = db.Column(db.Date)
	manager = db.Column(db.Integer)
	Date_2 = db.Column(db.Date)

	# 外键名称
	user_id_fk = db.relationship('SC_User',foreign_keys=[user_id], backref = db.backref('user_id_fk', lazy = 'dynamic'))

	def __init__(self,officer_level,assess_date,bq_dkye,bq_ghs,bq_khs,bq_lxsr,bq_zsbs,
		bm_dkye,bm_ghs,bm_lrgxd,gr_dkye,gr_ghs,gr_xzkhs,gr_zsbs,gr_lrgxd,
		rcxwpg,yql,total,result,qtpj,xq_dkye,xq_ghs,xq_xzkhs,xq_lxsr,xq_zsbs,
		user_id,date_1,manager,date_2):
		self.officer_level = db.Column(db.Integer)
		self.assess_date = db.Column(db.Date)
		self.bq_dkye = db.Column(db.String(4))
		self.bq_ghs = db.Column(db.String(4))
		self.bq_khs = db.Column(db.String(4))
		self.bq_lxsr = db.Column(db.String(4))
		self.bq_zsbs = db.Column(db.String(4))
		self.bm_dkye = db.Column(db.String(4))
		self.bm_ghs = db.Column(db.String(4))
		self.bm_lrgxd = db.Column(db.String(4))
		self.gr_dkye = db.Column(db.String(4))
		self.gr_ghs = db.Column(db.String(4))
		self.gr_xzkhs = db.Column(db.String(4))
		self.gr_zsbs = db.Column(db.String(4))
		self.gr_lrgxd = db.Column(db.String(4))
		self.rcxwpg = db.Column(db.String(4))
		self.yql = db.Column(db.String(16))
		self.total = db.Column(db.String(4))
		self.result = db.Column(db.Integer)
		self.qtpj = db.Column(db.String(255))
		self.xq_dkye = db.Column(db.String(16))
		self.xq_ghs = db.Column(db.String(16))
		self.xq_xzkhs = db.Column(db.String(16))
		self.xq_lxsr = db.Column(db.String(16))
		self.xq_zsbs = db.Column(db.String(16))
		self.user_id = user_id
		self.date_1 = date_1
		self.manager = manager
		self.date_2 = date_2

	def add(self):
		db.session.add(self)

  
