# coding:utf-8
from scapp import db
from flask.ext.login import current_user

#培训期最终考核表
class SC_Kpi_Train_Final(db.Model):
	__tablename__ = 'sc_kpi_train_final'
	id = db.Column(db.Integer, primary_key=True)
	job_tendency = db.Column(db.String(255))
	training_cycle = db.Column(db.String(4))
	job_final = db.Column(db.String(255))
	score_1 = db.Column(db.String(4))
	score_2 = db.Column(db.String(4))
	score_3 = db.Column(db.String(4))
	score_4 = db.Column(db.String(4))
	total_score = db.Column(db.String(4))
	avg_score = db.Column(db.String(8))
	zpj = db.Column(db.String(255))
	is_ok = db.Column(db.Integer)
	jyyqw = db.Column(db.String(255))
	user_id = db.Column(db.Integer)
	date_1 = db.Column(db.DateTime)
	manager = db.Column(db.Integer)
	date_2 = db.Column(db.DateTime)

	def __init__(self,user_id):
		self.user_id = user_id

	def add(self):
		db.session.add(self)