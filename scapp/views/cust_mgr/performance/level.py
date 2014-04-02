# coding:utf-8
from flask import Module, session, request, render_template, redirect, url_for
from flask.ext.login import login_user, logout_user, current_user, login_required
from scapp import app,db
from scapp.logic.performanceMapper import Level
from scapp.models import SC_User
from scapp.models import SC_UserRole
from scapp.models.performance.sc_performance_list import SC_performance_list 
import datetime




# 级别定义——搜索
@app.route('/Performance/khjlgl/jbdy_search', methods=['GET'])
def jbdy_search():
	return render_template("Performance/khjlgl/jbdy_search.html")

# 级别定义——列表
@app.route('/Performance/khjlgl/jbdy/<int:page>', methods=['POST'])
def jbdy(page):
	level = Level()
	data = level.queryList(request)
	return render_template("Performance/khjlgl/jbdy.html",data=data,level_id = request.form['level_id']
		,manager_name = request.form['manager_name'])

# 级别定义——修改
@app.route('/Performance/khjlgl/edit', methods=['POST'])
def edit():
	user_id = request.form['user_id']
	option_id = request.form['option_id']
	level = Level()
	level.edit(user_id,option_id)
	data = level.queryList(request)
	return render_template("Performance/khjlgl/jbdy.html",data=data,level_id=request.form['level_id'],
			manager_name=request.form['manager_name'])

# 层级查询——搜索
@app.route('/Performance/khjlgl/cjcx_search', methods=['GET'])
def cjcx_search():
    return render_template("Performance/khjlgl/cjcx_search.html")


# 层级查询——列表
@app.route('/Performance/khjlgl/cjcx/<int:page>', methods=['POST'])
def cjcx(page):
	level = Level()
	data = level.queryPerform(request)
	return render_template("Performance/khjlgl/cjcx.html",data=data)

# 晋级审核列表
@app.route('/Performance/khjlgl/jjshlist', methods=['GET'])
def jjshlist():
	level = Level()
	data = level.queryRise()
	return render_template("Performance/khjlgl/jjshlist.html",data=data)

# 晋级审核修改
@app.route('/Performance/level/edit', methods=['POST'])
def editRise():
	manager_id = request.form['user_id']
	apply_type = request.form['apply_type']
	level_id = request.form['level_id']
	apply_result = request.form['apply_result']
	level = Level()
	data = level.editRise(manager_id,apply_type,level_id,apply_result)
	return redirect('/Performance/khjlgl/jjshlist')