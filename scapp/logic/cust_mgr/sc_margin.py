#coding:utf-8
from flask.ext.login import login_user, logout_user, current_user, login_required,flash

from scapp.models.performance.sc_risk_margin import SC_risk_margin
from scapp.models.performance.sc_risk_margin_list import SC_risk_margin_list
from scapp import db
from scapp.config import logger
from scapp.config import PER_PAGE
from scapp.models import SC_User,SC_UserRole


class Margin():
	def getMarginList(self,page,request):
		user_id = request.form['user_id']
		sql="1=1"
		if user_id:
			sql += " and manager_id="+user_id
		data = SC_risk_margin.query.filter(sql).paginate(page, per_page = PER_PAGE)
		return data
	def getMarginListByPerson(self,user_id):
		data = SC_risk_margin.query.filter_by(manager_id=user_id).first()
		return data
	def getMarginByPerson(self,page,manager_id):
		data = SC_risk_margin_list.query.filter_by(manager_id=manager_id).order_by("id").paginate(page, per_page = PER_PAGE)
		return data