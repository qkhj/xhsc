#coding:utf-8
from flask.ext.login import login_user, logout_user, current_user, login_required,flash

from scapp.models.performance.sc_payment_list import SC_payment_list 
from scapp.models.performance.sc_business_error_list import SC_business_error_list 
from scapp.models.cust_mgr.sc_sta_mlm import SC_Sta_Mlm 
from scapp import db
from scapp.config import logger
from scapp.config import PER_PAGE
from scapp.models import SC_User,SC_UserRole
from scapp.models import SC_Privilege


class Payment():
	#获得工资单
	def getPaymentByPerson(self,page,request,user_id):
		beg_time = request.form['beg_time'] + " 00:00:00"
		end_time = request.form['end_time'] + " 23:59:59"
		sql = "payment_time between '"+beg_time+"' and '"+end_time+"'"
		sql += " and manager_id="+str(user_id)
		data = SC_payment_list.query.filter(sql).order_by("payment_time asc").paginate(page, per_page = PER_PAGE)
		return data
	def getPaymentByQuery(self,page,request):
		beg_time = request.form['beg_time'] + " 00:00:00"
		end_time = request.form['end_time'] + " 23:59:59"
		user_id = request.form['user_id']
		sql = "payment_time between '"+beg_time+"' and '"+end_time+"'"
		if user_id:
			sql += " and manager_id="+user_id
		data = SC_payment_list.query.filter(sql).order_by("payment_time asc").paginate(page, per_page = PER_PAGE)
		return data

	#薪酬计算
	def payroll(self,user_id,date,score):
		today = date.strftime('%Y')+"-"+date.strftime('%m')
		try:
	    	#客户经理工资计算
			role = SC_UserRole.query.filter_by(user_id=user_id).first().role
			role_level = role.role_level #取得用户权限等级
	        #客户经理
			if role_level==2:
	            #查询所处层级
				data = SC_Privilege.query.filter_by(priviliege_master_id=user_id,privilege_master="SC_User",priviliege_access
	                ="sc_account_manager_level").first()
				level_id = data.priviliege_access_value
				#查询基本工资
				parameter = SC_parameter_configure.query.filter_by(level_id=level_id).first()
				base_payment = parameter.base_payment
				#查询上月绩效
				sql = "SELECT sum(sum1) as total FROM (( SELECT sum(singel_performance) AS sum1"
				sql +=" FROM sc_loan_income_list WHERE DATE_FORMAT(create_time, '%%Y-%%M') = DATE_FORMAT("+date+", '%%Y-%%M'))"
				sql +=" UNION (SELECT sum(singel_performance_A) AS sum1 FROM sc_loan_income_list WHERE"
				sql +=" DATE_FORMAT(create_time, '%%Y-%%M') = DATE_FORMAT("+date+", '%%Y-%%M'))"
				sql +=" UNION (SELECT sum(singel_performance_B) AS sum1 FROM sc_loan_income_list WHERE"
				sql +=" DATE_FORMAT(create_time, '%%Y-%%M') = DATE_FORMAT("+date+", '%%Y-%%M'))) AS p"
				last_performance = db.engine.execute(sql).first()
	            #获取当月利息，逾期率等参数
				mlmSql = "user_id="+user_id
				mlmSql+=" and DATE_FORMAT(month, '%%Y-%%M')="+today
				mlm_list = SC_Sta_Mlm.query.filter(mlmSql).first()
				#当月逾期金额
				M=mim_list.overdue_amount
				r=0.8
				last_performance_result=last_performance.total+float(parameter.A2)+float((mlm_list.intrest)*(parameter.A3/100)*parameter.R*r)-M

	            #计算最终绩效(评估后)
				if score<60:
					last_performance_result=0
				elif score>=60 and score<100:
					last_performance_result=last_performance_result
				else:
					last_performance_result=int(last_performance_result)*1.05
				#当月总工资
				old_total_payment = base_payment+last_performance_result
				year = date.strftime('%Y')
				month = date.strftime('%m')
				#获取3月前日期
				if month<4:
					year=year-1
					if month==1:
						month=10
					elif month==2:
						month=11
					else:
						month=12
				old_3_date = str(year)+"-"+str(month)
				#获取3月前逾期金额
				mlm3Sql = "user_id="+user_id
				mlm3Sql+=" and DATE_FORMAT(month, '%%Y-%%M')="+old_3_date
				mlm3_list = SC_Sta_Mlm.query.filter(mlm3Sql).first()
				#如果总保险金低于逾期扣款
				nega_margin=0
				#风险保证金实体
				margin = SC_risk_margin.query.filter_by(anager_id=user_id).first()
				if mlm3_list:
					#逾期保险金增加，总保险金减少
					margin.overduce_margin=int(margin.overduce_margin)+mlm3_list.overdue_amount
					if int(margin.total_margin)>=mlm3_list.overdue_amount:               
					    margin.total_margin=int(margin.total_margin)-mlm3_list.overdue_amount
					else:
					    margin.total_margin=0
					    nega_margin=mlm3_list.overdue_amount-int(margin.total_margin)
					#新增逾期记录
					SC_risk_margin_list(user_id,date,mlm3_list.overdue_amount,2,margin.total_margin).add()
	                
	            #计算需缴纳风险保证金
				pay_margin=0
				if old_total_payment<=2000:
					pay_margin = 0
				elif old_total_payment>2000:
					if old_total_payment>5000:
						pay_margin+=(5000-2000)*0.3
						if old_total_payment>8000:
							pay_margin+=(8000-5000)*0.4
							pay_margin+=(old_total_payment-8000)*0.5
						else:
							pay_margin+=(old_total_payment-5000)*0.3
					else:
						pay_margin+=(old_total_payment-2000)*0.3
				#总保证金变化
				margin.total_margin=margin.total_margin+pay_margin
				#新增风险保险金记录
				SC_risk_margin_list(user_id,date,pay_margin,1,margin.total_margin).add()
				#获取3年前日期
				old_date = str(year-3)+"-"+str(month)
				#返还保证金
				return_margin=0
				if margin.total_margin>=50000:
					riskSql = "manager_id="+user_id
					riskSql+=" and DATE_FORMAT(payment_time, '%%Y-%%M')="+old_date
					riskSql+=" and inout_type=1"
					margin_list = SC_risk_margin_list.query.filter(riskSql).first()
					if margin_list:
						#达到返还要求,获得返还值
						return_margin = margin_list.inout_payment
						#返还总保证金
						margin.given_margin = margin.given_margin+return_margin
						#扣除总值小于逾期总值
						if margin.deduct_margin<margin.overduce_margin:
							if margin.deduct_margin+return_margin<=margin.overduce_margin:
								return_margin=0
								#最终所扣保险金=原先所扣保险金+返还
								margin.deduct_margin = margin.deduct_margin+return_margin
							else:
								return_margin=margin.deduct_margin+return_margin-margin.overduce_margin
								margin.deduct_margin = margin.overduce_margin
						margin.total_margin=margin.total_margin-return_margin
						#新增返还风险保险金记录
						SC_risk_margin_list(user_id,date,return_margin,3,margin.total_margin).add()
				#最终工资计算
				last_payment = old_total_payment-pay_margin+return_margin-nega_margin
				SC_payment_list(user_id,date,base_payment,last_performance.total,score,
	                last_performance_result,pay_margin,return_margin,M,last_payment).add()
			db.session.commit()
		except:
			# 回滚
			db.session.rollback()
			logger.exception('exception')

		#后台岗工资统计
		#查询总客户经理人数
		userData = SC_UserRole.query.filter("role.role_level=2").all()
		#查询当月已计算工资人数
		sql="DATE_FORMAT(payment_time, '%%Y-%%M')="+today
		paymentData = SC_payment_list.query.filter(sql).all()
		if len(userData)==len(paymentData):
			backPayment(date,paymentData)

	#后台岗工资计算
	def backPayment(self,date,paymentData):
		try:
			today = date.strftime('%Y')+"-"+date.strftime('%m')
			#计算客户经理总绩效
			total =0
			for i in range(len(paymentData)): 
				total+=paymentData[i].last_performance
			#计算平均绩效
			arg = float(total/len(paymentData))

			#获取所有后台岗人员
			userData = SC_UserRole.query.filter("role.role_level=3").all()
			for i in range(len(userData)):
				manager_id = userData[i].user.id 
				parameter = SC_parameter_configure.query.first()
				if parameter:
					#后台岗基本工资
					base_payment = parameter.back_payment
					#计算业务差错
					sql="manager_id="+manager_id
					sql+=" and DATE_FORMAT(create_time, '%%Y-%%M')="+today
					errorData = SC_business_error_list.query.filter(sql).all()
					
					#计算总工资
					old_total_payment = base_payment+arg/2
					#风险保证金实体
					margin = SC_risk_margin.query.filter_by(manager_id=user_id).first()
					if errorData:
						#需扣差错
						errorSum = errorData*20
						#逾期保险金增加，总保险金减少
						margin.overduce_margin=int(margin.overduce_margin)+errorSum
						#新增逾期记录
						SC_risk_margin_list(user_id,date,errorSum,2,margin.total_margin).add()
		            #计算需缴纳风险保证金
					pay_margin=0
					if old_total_payment<=2000:
						pay_margin = 0
					elif old_total_payment>2000:
						if old_total_payment>5000:
							pay_margin+=(5000-2000)*0.3
							if old_total_payment>8000:
								pay_margin+=(8000-5000)*0.4
								pay_margin+=(old_total_payment-8000)*0.5
							else:
								pay_margin+=(old_total_payment-5000)*0.3
						else:
							pay_margin+=(old_total_payment-2000)*0.3
					#总保证金变化
					
					margin.total_margin=margin.total_margin+pay_margin
					#新增风险保险金记录
					SC_risk_margin_list(user_id,date,pay_margin,1,margin.total_margin).add()
					#获取3年前日期
					old_date = str(date.strftime('%Y')-3)+"-"+str(date.strftime('%m'))
					#返还保证金
					return_margin=0
					if margin.total_margin>=30000:
						riskSql = "manager_id="+user_id
						riskSql+=" and DATE_FORMAT(payment_time, '%%Y-%%M')="+old_date
						riskSql+=" and inout_type=1"
						margin_list = SC_risk_margin_list.query.filter(riskSql).first()
						if margin_list:
							#达到返还要求,获得返还值
							return_margin = margin_list.inout_payment
							margin.given_margin=margin.given_margin+return_margin
							#所扣总值小于逾期总值
							if margin.deduct_margin<margin.overduce_margin:
								if margin.deduct_margin+return_margin<=margin.overduce_margin:
									return_margin=0
									#最终所扣保险金=原先所扣保险金+返还
									margin.deduct_margin = margin.deduct_margin+return_margin
								else:
									return_margin=margin.deduct_margin+return_margin-margin.overduce_margin
									margin.deduct_margin = margin.overduce_margin
							margin.total_margin=margin.total_margin-return_margin
							#新增返还风险保险金记录
							SC_risk_margin_list(user_id,date,return_margin,3,margin.total_margin).add()
							#最终工资计算
							last_payment = old_total_payment-pay_margin+return_margin-nega_margin
							SC_payment_list(user_id,date,base_payment,arg/2,"",
		            			arg/2,pay_margin,return_margin,errorSum,last_payment).add()
		        			db.session.commit()
		except:
			# 回滚
			db.session.rollback()
			logger.exception('exception')