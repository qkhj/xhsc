#coding:utf-8
from apscheduler.scheduler import Scheduler  
import datetime
from scapp import db
from scapp.config import logger

from scapp.models.performance.sc_assess_record import SC_assess_record 
from scapp.models.performance.sc_performance_list import SC_performance_list 
from scapp.models.performance.sc_examine_rise import SC_examine_rise
from scapp.models.performance.sc_manager_level_index import SC_manager_level_index 


class timing():

	def __init__(self):
		sched = Scheduler()
		sched.daemonic = False
		sched.add_cron_job(self.rise,month='4,7,10,12',day='1')  
		sched.add_cron_job(self.kpi,month='1-12',day='1',hour='2')  #每月1号凌晨2点创建当月评估表
		sched.start()

	#晋降级线程
	def rise(self):
		try:
			year = datetime.date.today().strftime('%Y')
			month = datetime.date.today().strftime('%m')
			if month==1:
				year = year-1
				month = 12
			else:
				month=month
			search_date = str(year)+"-"+str(month)
		   	sql = "select sc_user.id as id from sc_userrole,sc_role,sc_user where "
			sql +=" sc_userrole.role_id=sc_role.id and sc_role.role_level=2 and sc_user.id=sc_userrole.user_id"
			data = db.engine.execute(sql).fetchall()
			for i in range(len(data)):
				assess = SC_assess_record.query.filter_by(manager_id=data[i].id).first()
				if assess:
					if assess.assess_sum=='3':
						#获取客户经理上月业绩
						achieve = SC_performance_list.query.filter("manager_id="+str(data[i].id)+" and DATE_FORMAT(month, '%Y-%m')='"+search_date+"'").first()
						if int(assess.assess_arg)>90:
							if achieve:
								if not achieve.level_id==6:
									#获取高一层级考核业绩
									base_achieve = SC_manager_level_index.query.filter_by(level_id=int(achieve.level_id)+1).first()
									if float(achieve.count)>float(base_achieve.count) and float(achieve.valid_sum)>float(base_achieve.valid_sum) and float(achieve.balance_scale)>float(base_achieve.balance_scale):
										SC_examine_rise(data[i].id,search_date,"1","1").add()
									else:
										if not achieve.level_id==1:
											#获取低一层级考核业绩
											base_achieve = SC_manager_level_index.query.filter_by(level_id=int(achieve.level_id)-1).first()
											if float(achieve.count)<float(base_achieve.count) and float(achieve.valid_sum)<float(base_achieve.valid_sum) and float(achieve.balance_scale)<float(base_achieve.balance_scale):
												SC_examine_rise(data[i].id,search_date,"2","1").add()
						else:
							if not achieve.level_id==1:
								#获取低一层级考核业绩
								base_achieve = SC_manager_level_index.query.filter_by(level_id=int(achieve.level_id)-1).first()
								if float(achieve.count)<float(base_achieve.count) and float(achieve.valid_sum)<float(base_achieve.valid_sum) and float(achieve.balance_scale)<float(base_achieve.balance_scale):
									SC_examine_rise(data[i].id,search_date,"2","1").add()
			# 事务提交
			db.session.commit()
		except:
			# 回滚
			db.session.rollback()
			logger.exception('exception')


	#每月初创建当月评估表
	def kpi(self):
		try:
			sql = "SELECT sc_user.id,sc_role.role_level FROM sc_userrole "
			sql += "INNER JOIN sc_role ON sc_userrole.role_id = sc_role.id "
			sql += "INNER JOIN sc_user ON sc_user.id = sc_userrole.user_id "
			sql += "where sc_role.role_level >= 2"
			users = db.session.execute(sql)

			now = datetime.datetime.now().date()

			for obj in users:
				if obj.role_level == 2:#客户经理
					insert_sql = "insert into sc_kpi_officer (user_id,assess_date) values ("+obj.id+",'"+now+"'')"
					db.session.execute(insert_sql)
				elif obj.role_level == 3:#运营岗
					insert_sql = "insert into sc_kpi_yunying (user_id,assess_date) values ("+obj.id+",'"+now+"'')"
					db.session.execute(insert_sql)

			# 事务提交
			db.session.commit()
		except:
			# 回滚
			db.session.rollback()
			logger.exception('exception')