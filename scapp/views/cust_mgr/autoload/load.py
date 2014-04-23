#coding:utf-8
import datetime
from scapp import db
from scapp.config import logger

from scapp.models.performance.sc_assess_record import SC_assess_record 
from scapp.models.performance.sc_performance_list import SC_performance_list 
from scapp.models.performance.sc_examine_rise import SC_examine_rise
from scapp.models.performance.sc_manager_level_index import SC_manager_level_index 
from scapp.models import SC_Privilege
from scapp.models.performance.sc_parameter_configure import SC_parameter_configure
from scapp.models import SC_Loan_Apply
from scapp.models import SC_Approval_Decision
from scapp.models.performance.sc_loan_income_list import SC_loan_income_list 
class scriptload():
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

			now = datetime.datetime.now().date().strftime("%Y-%m-%d")

			for obj in users:
				if obj.role_level == 2:#客户经理
					insert_sql = "insert into sc_kpi_officer (user_id,assess_date) values ("+str(obj.id)+",'"+now+"')"
					db.session.execute(insert_sql)
				elif obj.role_level == 3:#运营岗
					insert_sql = "insert into sc_kpi_yunying (user_id,assess_date) values ("+str(obj.id)+",'"+now+"')"
					db.session.execute(insert_sql)

			# 事务提交
			db.session.commit()
		except:
			# 回滚
			db.session.rollback()
			logger.exception('exception')

	#创建上月余额规模
	def total(self):
		try:
			d1 = datetime.datetime.now()
			d3 = d1 - datetime.timedelta(hours=24)
			last_day = d3.strftime("%Y")+"-"+d3.strftime("%m")
			sql="select a.user_id as id from sc_userrole a,sc_role b where a.role_id=b.id and b.role_level=2"
			data = db.session.execute(sql)
			for obj in data:
				loan_sql = "select sum(a.loan_balance) as loanSum from sc_bank_loans_main a,sc_loan_apply b where a.loan_apply_id=b.id and b.A_loan_officer="+str(obj.id)
				dataSum = db.session.execute(loan_sql).fetchall()
				#上月余额规模
				for i in dataSum:
					lastSum = i.loanSum
					update_sql="DATE_FORMAT(month, '%Y-%m')='"+last_day+"'"
					update_sql+=" and manager_id="+str(obj.id)
					performanc_list = SC_performance_list.query.filter(update_sql).first()
					if performanc_list:
						performanc_list[j].balance_scale=lastSum
			# 事务提交
			db.session.commit()
		except:
			# 回滚
			db.session.rollback()
			logger.exception('exception')

	#初始化当月业绩表
	def perform(self):
		try:	
			today = datetime.datetime.now().strftime('%Y')+"-"+datetime.datetime.now().strftime('%m')
			sql="select a.user_id as id from sc_userrole a,sc_role b where a.role_id=b.id and b.role_level=2"
			data = db.session.execute(sql)
			for obj in data:
				#获取层级
				level = SC_Privilege.query.filter_by(priviliege_master_id=obj.id,privilege_master="SC_User",
					priviliege_access="sc_account_manager_level").first()
				level_id=0
				if level:
					level_id = level.priviliege_access_value
				insert_sql="DATE_FORMAT(month, '%Y-%m')='"+today+"'"
				insert_sql+=" and manager_id="+str(obj.id)
				performanc_list = SC_performance_list.query.filter(insert_sql).first()
				if not performanc_list:
					SC_performance_list(datetime.datetime.now(),obj.id,0,0,0,0,level_id).add()
			db.session.commit()
		except:
			# 回滚
			db.session.rollback()
			logger.exception('exception')

	#统计每笔贷款所得笔数绩效
	def first(self):
		try:
			sql ="select a.* from sc_approval_decision a,sc_loan_apply b where a.loan_apply_id=b.id and b.process_status='601' and a.loan_apply_id not in (select loan_apply_id from sc_loan_income_list)"
			data = db.session.execute(sql)
			for obj in data:
				#获取放贷日期
				lending_date = obj.loan_date
				#计算绩效日期
				year = int(lending_date.strftime('%Y'))
				month = int(lending_date.strftime('%m'))
				if month==12:
				    year = year+1
				    month=1
				payment_date = datetime.date(year,month,1)
				#折算笔数
				inCount = self.amount(int(obj.amount))
				#查询层级
				loan_apply = SC_Loan_Apply.query.filter_by(id=obj.loan_apply_id).first()
				level = SC_Privilege.query.filter_by(priviliege_master_id=loan_apply.A_loan_officer,privilege_master="SC_User",priviliege_access="sc_account_manager_level").first()
				#查询所有绩效参数
				if level:
					parameter = SC_parameter_configure.query.filter_by(level_id=level.priviliege_access_value).first()
					#所得绩效
					if parameter:
						total = float(parameter.A1)*inCount
						yunying_total = total*0.1
						A_total = total*0.6
						B_total = total*0.3
						SC_loan_income_list(obj.loan_apply_id,loan_apply.yunying_loan_officer,yunying_total,loan_apply.A_loan_officer,
							A_total,loan_apply.B_loan_officer,B_total,payment_date).add()
		 	 # 事务提交
			db.session.commit()
		except:
			# 回滚
			db.session.rollback()
			logger.exception('exception')
	#折算笔数
	def amount(self,am):
	    if am<=50000:
	        return 0.7
	    elif am>50000 and am<=150000:
	        return 1
	    elif am>150000 and am<=300000:
	        return 1.5
	    elif am>300000 and am<=500000:
	        return 2
	    elif am>500000 and am<=1000000:
	        return 3
	    elif am>1000000 and am<=2000000:
	        return 3.5
	    elif am>2000000 and am<3000000:
	        return 4
	    elif am>3000000:
	        return 5
