#coding:utf-8
from flask.ext.login import login_user, logout_user, current_user, login_required,flash
from scapp.models import SC_UserRole
from scapp.models import SC_User
from scapp.models import SC_Loan_Apply
from scapp.models import SC_Approval_Decision
from scapp.pojo.waiting_work import Waiting
from scapp.config import PROCESS_STATUS_DKSQSH
from scapp.models import SC_Monitor
from scapp import db
from scapp.config import logger
from scapp.models import SC_Classify
from scapp.models import View_Query_Loan
from scapp.config import PER_PAGE

class Total():
#待办事项统计
	def getListSum(self, role):
		role_level = role.role_level
		waiting = Waiting()
		if role_level==1:
			counts = SC_Loan_Apply.query.filter("process_status="+PROCESS_STATUS_DKSQSH).count()
			waiting.dksqsh=counts
		if role_level==2:		
			sql = "A_loan_officer = "+str(current_user.id)+" or "
			sql+="B_loan_officer = "+str(current_user.id)+" or "
			sql+="yunying_loan_officer = "+str(current_user.id)+""
			counts1 = SC_Loan_Apply.query.filter(sql).count()
			waiting.dqdc=counts1
		return waiting

#新增标准
	def addNewBZ(self,loan_apply_id,request):
		try:
			monitor_date_list = request.form.getlist('monitor_date')
			monitor_type_list = request.form.getlist('monitor_type')
			monitor_content_list = request.form.getlist('monitor_content')
			monitor_remark_list = request.form.getlist('monitor_remark')
			for i in range(len(monitor_date_list)):
				SC_Monitor(loan_apply_id,monitor_date_list[i],monitor_type_list[i], monitor_content_list[i],monitor_remark_list[i]).add()
			db.session.commit()
			# 消息闪现
			flash('保存成功','success')
		except:
		    # 回滚
		    db.session.rollback()
		    logger.exception('exception')
		    # 消息闪现
		    flash('保存失败','error')
#删除所有标准
	def deleteBZ(self,loan_apply_id):
		SC_Monitor.query.filter_by(loan_apply_id=loan_apply_id).delete()
		db.session.flush()
#通过贷款单获取合同信息
	def getInformByloadId(self,loan_apply_id):
		pactInform = SC_Approval_Decision.query.filter_by(loan_apply_id=loan_apply_id).first()
		return pactInform
class User():
#获取用户名
	def getUserName(self,id):
		user = SC_User.query.filter_by(id=id).first()
		return user.login_name

class Property():
#保存资产质量分类
	def addProperty(self,loan_apply_id,index_add,classify):
		SC_Classify(loan_apply_id,index_add,classify,'',0).add()
		db.session.commit()

#查询最新质量分类
	def queryLastProperty(self,loan_apply_id):
		LastProperty = SC_Classify.query.filter_by(loan_apply_id=loan_apply_id).order_by("index_add desc").first()
		return LastProperty
#更新最新质量分类
	def updateLastProperty(self,loan_apply_id,index_add,classify):
		SC_Classify.query.filter_by(loan_apply_id=loan_apply_id,index_add=index_add).update({"classify":classify})
		db.session.commit()
#更新最新质量分类审核
	def updateLastPropertyBysh(self,loan_apply_id,index_add,is_pass):
		SC_Classify.query.filter_by(loan_apply_id=loan_apply_id,index_add=index_add).update({"is_pass":is_pass})
		db.session.commit()
#查询质量分类列表
	def queryList(self,customer_name,loan_type,classify,page):
		sql = " 1=1 "
		if loan_type != '0':
		    sql += " and loan_type='"+loan_type+"'"
		if classify != '0':
		    sql += " and classify='"+classify+"'"
		if customer_name:
		    sql += " and (company_customer_name like '%"+customer_name+"%' or individual_customer_name like '%"+customer_name+"%')"
		loan_apply = View_Query_Loan.query.filter(sql).paginate(page, per_page = PER_PAGE)
		return loan_apply