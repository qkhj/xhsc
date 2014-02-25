#coding:utf-8
from flask.ext.login import login_user, logout_user, current_user, login_required
from scapp.models import SC_UserRole
from scapp.models import SC_Loan_Apply
from scapp.pojo.waiting_work import Waiting
from scapp.config import PROCESS_STATUS_DKSQSH

class Total():
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