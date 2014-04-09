# coding:utf-8
from flask import Module, session, request, render_template, redirect, url_for
from flask.ext.login import login_user, logout_user, current_user, login_required
from scapp import app,db
from scapp.logic.performanceMapper import Level
from scapp.models import SC_User
from scapp.models import SC_UserRole
from scapp.models.performance.sc_performance_list import SC_performance_list 
import datetime
from scapp.logic.cust_mgr.sc_margin import Margin
from scapp.logic.cust_mgr.sc_payment import Payment


# 风险保证金——搜索
@app.route('/Performance/jxxc/fxbzj_search', methods=['GET'])
def fxbzj_search():
	# date= datetime.datetime.now()
	# pay = Payment()
	# pay.payroll(18,date,90)

	role = SC_UserRole.query.filter_by(user_id=current_user.id).first().role
	level = role.role_level #取得用户权限等级
	#普通员工
	if level==2 or level==3:
		margin = Margin()
		data = margin.getMarginListByPerson(current_user.id)
		return render_template("Performance/jxxc/fxbzj_person.html",data=data)
	else:
		user = SC_User.query.order_by("id").all()
    	return render_template("Performance/jxxc/fxbzj_search.html",user=user)

# 风险保证金
@app.route('/Performance/jxxc/fxbzj/<int:page>', methods=['POST'])
def fxbzj(page):
	margin = Margin()
	data = margin.getMarginList(page,request)
	return render_template("Performance/jxxc/fxbzj.html",data=data,user_id=request.form['user_id'])

# 风险保证金——详单
@app.route('/Performance/jxxc/fxbzj_list/<int:page>/<int:manager_id>', methods=['GET'])
def fxbzj_list(page,manager_id):
	margin = Margin()
	data = margin.getMarginByPerson(page,manager_id)
	return render_template("Performance/jxxc/fxbzj_list.html",data=data,manager_id=manager_id)
