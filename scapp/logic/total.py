#coding:utf-8
from flask.ext.login import login_user, logout_user, current_user, login_required,flash
from scapp.models import SC_UserRole
from scapp.models import SC_Loan_Apply
from scapp.pojo.waiting_work import Waiting
from scapp.config import PROCESS_STATUS_DKSQSH
from scapp.models import SC_Monitor
from scapp import db
from scapp.config import logger

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