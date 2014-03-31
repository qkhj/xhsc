# coding:utf-8
from flask import Module, session, request, render_template, redirect, url_for
from flask.ext.login import login_user, logout_user, current_user, login_required
from scapp import app,db
from scapp.models import SC_User
from scapp.models import SC_UserRole

from scapp.models import SC_Privilege



# 薪酬-搜索
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

#薪酬计算
def payroll(self,user_id,date):
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
        











