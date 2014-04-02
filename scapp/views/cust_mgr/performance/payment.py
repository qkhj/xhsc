# coding:utf-8
from flask import Module, session, request, render_template, redirect, url_for
from flask.ext.login import login_user, logout_user, current_user, login_required
from scapp import app,db
from scapp.models import SC_User
from scapp.models import SC_UserRole

from scapp.models import SC_Privilege
from scapp.models.performance.sc_loan_income_list import SC_loan_income_list 
from scapp.models.performance.sc_risk_margin_list import SC_risk_margin_list 
from scapp.models.performance.sc_risk_margin import SC_risk_margin 
from scapp.models.performance.sc_payment_list import SC_payment_list 
from scapp.logic.cust_mgr.sc_payment import Payment


# 个人薪酬——搜索
@app.route('/Performance/jxxc/grxc_search', methods=['GET'])
def grxc_search():
    role = SC_UserRole.query.filter_by(user_id=current_user.id).first().role
    level = role.role_level #取得用户权限等级
    if level==2 or level==3:
        return render_template("Performance/jxxc/grxc_search.html")
    else:
        user = SC_User.query.order_by("id").all()
        return render_template("Performance/jxxc/xccx_search.html",user=user)

# 个人薪酬
@app.route('/Performance/jxxc/grxc/<int:page>', methods=['POST'])
def grxc(page):
    role = SC_UserRole.query.filter_by(user_id=current_user.id).first().role
    level = role.role_level #取得用户权限等级
    payment = Payment()
    if level==2 or level==3:
        data = payment.getPaymentByPerson(page,request,current_user.id)
        return render_template("Performance/jxxc/grxc.html",data=data,beg_time = request.form['beg_time'],
            end_time = request.form['end_time'])
    else:
        data = payment.getPaymentByQuery(page,request)
        return render_template("Performance/jxxc/xccx.html",data=data,beg_time = request.form['beg_time'],
            end_time = request.form['end_time'],user_id = request.form['user_id'])










