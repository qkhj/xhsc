# coding:utf-8

import os

from flask import Module, session, request, render_template, redirect, url_for,flash
from flask.ext.login import current_user
from sqlalchemy.sql import or_ 
import datetime

from scapp import db
from scapp.config import logger
from scapp.config import PER_PAGE

from scapp.models import SC_User
from scapp.models import SC_UserRole
from scapp.models import SC_Industry
from scapp.models import SC_Regisiter_Type
from scapp.models import SC_Loan_Purpose
from scapp.models import SC_Target_Customer

from scapp.models import View_Get_Cus_Mgr

from scapp import app

# 客户分配
@app.route('/Information/khfp', methods=['GET'])
def Information_khfp():
    return render_template("Information/khfp/khfp_search.html")
	
# 客户分配
@app.route('/Information/khfp/khfp_search/<int:page>', methods=['GET','POST'])
def khfp_search(page):
    # 模糊查询
    customer_name = request.form['customer_name']
    beg_date = request.form['beg_date'] + " 00:00:00"
    end_date = request.form['end_date'] + " 23:59:59"

    sql = "create_date between '"+beg_date+"' and '"+end_date + "' "
    if customer_name:
        sql += " and (customer_name like '%"+customer_name+"%' or shop_name like '%"+customer_name+"%') "

    target_customer = SC_Target_Customer.query.filter(sql).order_by("id").paginate(page, per_page = PER_PAGE)

    users = View_Get_Cus_Mgr.query.filter("role_level>=2").order_by("id").all()#客户经理
    role = SC_UserRole.query.filter_by(user_id=current_user.id).first().role
    return render_template("Information/khfp/khfp.html",users=users,role=role,target_customer=target_customer,
        customer_name=customer_name,beg_date=request.form['beg_date'],end_date=request.form['end_date'])

# 编辑客户分配
@app.route('/Information/khfp/edit_khfp/<int:page>/<int:target_customer_id>/<int:user_id>', methods=['GET','POST'])
def edit_khfp(page,target_customer_id,user_id):

    try:
        # 模糊查询
        customer_name = request.form['customer_name']
        beg_date = request.form['beg_date'] + " 00:00:00"
        end_date = request.form['end_date'] + " 23:59:59"

        target_customer = SC_Target_Customer.query.filter_by(id=target_customer_id).first()

        target_customer.manager = current_user.id
        if user_id == 0:
            target_customer.loan_officer = None
            target_customer.loan_officer_date = datetime.datetime.now()
        else:
            target_customer.loan_officer = user_id
            target_customer.loan_officer_date = datetime.datetime.now()

        # 事务提交
        db.session.commit()
        # 消息闪现
        flash('保存成功','success')
    except:
        # 回滚
        db.session.rollback()
        logger.exception('exception')
        # 消息闪现
        flash('保存失败','error')

    sql = "create_date between '"+beg_date+"' and '"+end_date + "' "
    if customer_name:
        sql += " and (customer_name like '%"+customer_name+"%' or shop_name like '%"+customer_name+"%') "

    target_customer = SC_Target_Customer.query.filter(sql).order_by("id").paginate(page, per_page = PER_PAGE)

    users = SC_User.query.order_by("id").all()
    role = SC_UserRole.query.filter_by(user_id=current_user.id).first().role
    return render_template("Information/khfp/khfp.html",users=users,role=role,target_customer=target_customer,
        customer_name=customer_name,beg_date=request.form['beg_date'],end_date=request.form['end_date'])