# coding:utf-8
from scapp import db
from flask.ext.login import current_user

#在岗考核表-客户经理
class SC_Kpi_Yunying(db.Model):
	__tablename__ = 'sc_kpi_yunying'
	id = db.Column(db.Integer, primary_key=True)
	assess_date = db.Column(db.Date)
	bm_dkye = db.Column(db.String(4))
	bm_ghs = db.Column(db.String(4))
	bm_lrgxd = db.Column(db.String(4))
	gz_sjlr = db.Column(db.String(4))
	gz_ywtj = db.Column(db.String(4))
	gz_ht = db.Column(db.String(4))
	gz_fk = db.Column(db.String(4))
	gz_dagl = db.Column(db.String(4))
	gz_khgx = db.Column(db.String(4))
	gz_alzl = db.Column(db.String(4))
	gz_fxkz = db.Column(db.String(4))
	gz_rcxw = db.Column(db.String(4))
	gz_yql = db.Column(db.String(4))
	total = db.Column(db.String(4))
	result = db.Column(db.Integer)
	qtpj = db.Column(db.String(255))
	user_id = db.Column(db.Integer, db.ForeignKey('sc_user.id'))
	Date_1 = db.Column(db.Date)
	manager = db.Column(db.Integer)
	Date_2 = db.Column(db.Date)

	# 外键名称
	sc_kpi_yunying_ibfk_1 = db.relationship('SC_User',foreign_keys=[user_id], backref = db.backref('sc_kpi_yunying_ibfk_1', lazy = 'dynamic'))

	def __init__(self,assess_date,bm_dkye,bm_ghs,bm_lrgxd,gz_sjlr,gz_ywtj,gz_ht,gz_fk,
		gz_dagl,gz_khgx,gz_alzl,gz_fxkz,gz_rcxw,gz_yql,total,result,qtpj,
		user_id,date_1,manager,date_2):
		self.assess_date = db.Column(db.Date)
		self.bm_dkye = db.Column(db.String(4))
		self.bm_ghs = db.Column(db.String(4))
		self.bm_lrgxd = db.Column(db.String(4))
		self.gz_sjlr = db.Column(db.String(4))
		self.gz_ywtj = db.Column(db.String(4))
		self.gz_ht = db.Column(db.String(4))
		self.gz_fk = db.Column(db.String(4))
		self.gz_dagl = db.Column(db.String(4))
		self.gz_khgx = db.Column(db.String(4))
		self.gz_alzl = db.Column(db.String(4))
		self.gz_fxkz = db.Column(db.String(4))
		self.gz_rcxw = db.Column(db.String(4))
		self.gz_yql = db.Column(db.String(4))
		self.total = db.Column(db.String(4))
		self.result = db.Column(db.Integer)
		self.qtpj = db.Column(db.String(255))
		self.user_id = user_id
		self.date_1 = date_1
		self.manager = manager
		self.date_2 = date_2

	def add(self):
		db.session.add(self)

  
