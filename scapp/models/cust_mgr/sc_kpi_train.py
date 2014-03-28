# coding:utf-8
from scapp import db
from flask.ext.login import current_user

#培训期课堂纪律考核表
class SC_Kpi_Train(db.Model):
	__tablename__ = 'sc_kpi_train'
	id = db.Column(db.Integer, primary_key=True)
	train_date = db.Column(db.Date)#培训时间
	job_tendency = db.Column(db.String(255))#岗位倾向
	class_hour = db.Column(db.String(4))#学时
	cqqk_1 = db.Column(db.String(4))#出勤
	cqqk_2 = db.Column(db.String(4))#出勤
	ktjl_1 = db.Column(db.String(4))#课堂纪律
	ktjl_2 = db.Column(db.String(4))#课堂纪律
	ktfy_1 = db.Column(db.String(4))#课堂发言
	ktfy_2 = db.Column(db.String(4))#课堂发言
	ktcs_1 = db.Column(db.String(4))#课堂测试
	ktcs_2 = db.Column(db.String(4))#课堂测试
	mnbx_1 = db.Column(db.String(4))#模拟表现
	mnbx_2 = db.Column(db.String(4))#模拟表现
	ztbx_1 = db.Column(db.String(4))#专题表现
	ztbx_2 = db.Column(db.String(4))#专题表现
	jszs_1 = db.Column(db.String(4))#技术知识
	jszs_2 = db.Column(db.String(4))#技术知识
	tdxz_1 = db.Column(db.String(4))#团队合作
	tdxz_2 = db.Column(db.String(4))#团队合作
	xtgt_1 = db.Column(db.String(4))#沟通协调
	xtgt_2 = db.Column(db.String(4))#沟通协调
	jyks_1 = db.Column(db.String(4))#结业考试
	jyks_2 = db.Column(db.String(4))#结业考试
	total = db.Column(db.String(4))#综合得分
	result = db.Column(db.Integer)#评估结果(1 优秀 2 良好 3 及格 4 不及格)
	performance = db.Column(db.String(255))#综合表现
	focus_on = db.Column(db.String(255))#重点关注
	next_work_target = db.Column(db.String(255))#下棋工作指标
	individual_expectations = db.Column(db.String(255))#个人期望
	user_id = db.Column(db.Integer)
	date_1 = db.Column(db.Date)
	manager = db.Column(db.Integer)
	date_2 = db.Column(db.Date)
	bank_director = db.Column(db.Integer)
	date_3 = db.Column(db.Date)

	def __init__(self,train_date,job_tendency,class_hour,cqqk_1,cqqk_2,ktjl_1,ktjl_2,ktfy_1,ktfy_2,ktcs_1,ktcs_2,
		mnbx_1,mnbx_2,ztbx_1,ztbx_2,jszs_1,jszs_2,tdxz_1,tdxz_2,xtgt_1,xtgt_2,jyks_1,jyks_2,
		total,result,performance,focus_on,next_work_target,individual_expectations,
		user_id,date_1,manager,date_2):
		self.train_date = train_date
		self.job_tendency = job_tendency
		self.class_hour = class_hour
		self.cqqk_1 = cqqk_1
		self.cqqk_2 = cqqk_2
		self.ktjl_1 = ktjl_1
		self.ktjl_2 = ktjl_2
		self.ktfy_1 = ktfy_1
		self.ktfy_2 = ktfy_2
		self.ktcs_1 = ktcs_1
		self.ktcs_2 = ktcs_2
		self.mnbx_1 = mnbx_1
		self.mnbx_2 = mnbx_2
		self.ztbx_1 = ztbx_1
		self.ztbx_2 = ztbx_2
		self.jszs_1 = jszs_1
		self.jszs_2 = jszs_2
		self.tdxz_1 = tdxz_1
		self.tdxz_2 = tdxz_2
		self.xtgt_1 = xtgt_1
		self.xtgt_2 = xtgt_2
		self.jyks_1 = jyks_1
		self.jyks_2 = jyks_2
		self.total = total
		self.result = result
		self.performance = performance
		self.focus_on = focus_on
		self.next_work_target = next_work_target
		self.individual_expectations = individual_expectations
		self.user_id = user_id
		self.date_1 = date_1
		self.manager = manager
		self.date_2 = date_2

	def add(self):
		db.session.add(self)