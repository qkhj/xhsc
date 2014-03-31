# coding:utf-8
from flask import Module, session, request, render_template, redirect, url_for
from flask.ext.login import login_user, logout_user, current_user, login_required
from scapp import app,db
from scapp.logic.performanceMapper import Business
from scapp.models import SC_User
from scapp.models import SC_UserRole



# 业务差错列表-搜索
@app.route('/Performance/jxxc/ywcctj_search', methods=['GET'])
def ywcctj_search():
    role = SC_UserRole.query.filter_by(user_id=current_user.id).first().role
    level = role.role_level #取得用户权限等级
    #普通员工
    if level==2 or level==3:
    	# business = Business()
    	# data = business.queryByPerson(current_user.id,1)
    	return render_template("Performance/jxxc/ywcctj_search_common.html")
    else:
		return render_template("Performance/jxxc/ywcctj_search.html")

# 业务差错统计
@app.route('/Performance/jxxc/ywcctj/<int:page>', methods=['POST'])
def ywcctj(page):
    role = SC_UserRole.query.filter_by(user_id=current_user.id).first().role
    level = role.role_level #取得用户权限等级
    business = Business()
    data = ""
    if level==2 or level==3:
        data = business.queryByPerson(current_user.id,page,request)
        return render_template("Performance/jxxc/ywcctj_common.html",data=data,beg_time = request.form['beg_time'],
            end_time = request.form['end_time'])
    else:
        data = business.query(page,request)
        return render_template("Performance/jxxc/ywcctj.html",data=data,beg_time = request.form['beg_time'],
    		end_time = request.form['end_time'],name = request.form['name'])

# 业务差错新增页面
@app.route('/Performance/jxxc/new_ywcc', methods=['GET'])
def new_ywcc():
	user = SC_User.query.order_by("id").all()
	return render_template("Performance/jxxc/new_ywcc.html",user=user)

# 业务差错新增
@app.route('/Performance/jxxc/addError', methods=['POST'])
def addError():
	business = Business()
	business.addError(request)
	return render_template("Performance/jxxc/ywcctj_search.html")


