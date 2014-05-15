# coding:utf-8

import os

from flask import Module, session, request, render_template, redirect, url_for,flash
from flask.ext.login import current_user
import datetime

from scapp import db
from scapp.config import logger
from scapp.config import PER_PAGE

from scapp.config import PROCESS_STATUS_DKFKJH

from scapp.models import SC_User
from scapp.models import SC_UserRole
from scapp.models import View_Get_Cus_Mgr
from scapp.models import View_Query_Loan
from scapp.models import View_Loan_Repayment

from scapp import app

from scapp.models import SC_Loan_Product

# 还款登记
@app.route('/Process/hkdj/hkdj', methods=['GET'])
def Process_hkdj():
	user = View_Get_Cus_Mgr.query.filter("role_level>=2").order_by("id").all()#客户经理
	role = SC_UserRole.query.filter_by(user_id=current_user.id).first().role
	
	loan_product = SC_Loan_Product.query.all()
	
	return render_template("Process/hkdj/hkdj_search.html",user=user,role=role,loan_product=loan_product)

# 还款登记搜索
@app.route('/Process/hkdj/hkdj_search/<int:page>', methods=['POST'])
def hkdj_search(page):
	manager = request.form['manager']
	customer_name = request.form['customer_name']
	loan_type = request.form['loan_type']
	sql = "process_status='"+PROCESS_STATUS_DKFKJH+"'"
	if manager != '0':
		sql += " and marketing_loan_officer="+manager
	if loan_type != '0':
	    sql += " and loan_type='"+loan_type+"'"

	if customer_name:
	    sql += " and (company_customer_name like '%"+customer_name+"%' or individual_customer_name like '%"+customer_name+"%')"

	loan_apply = View_Query_Loan.query.filter(sql).paginate(page, per_page = PER_PAGE)

	user = SC_User.query.all()#客户经理
	
	loan_product = SC_Loan_Product.query.all()
	
	return render_template("Process/hkdj/hkdj.html",loan_apply=loan_apply,customer_name=customer_name,
		loan_type=loan_type,manager=manager,user=user,loan_product=loan_product)
	
# 还款登记——编辑还款登记
@app.route('/Process/hkdj/edit_hkdj/<int:loan_apply_id>', methods=['GET'])
def edit_hkdj(loan_apply_id):
	loan_apply = View_Query_Loan.query.filter_by(loan_apply_id=loan_apply_id).first()
	loan_repayment = View_Loan_Repayment.query.filter_by(id=loan_apply_id).all()
	
	loan_product = SC_Loan_Product.query.all()
	
	return render_template("Process/hkdj/edit_hkdj.html",loan_apply=loan_apply,loan_repayment=loan_repayment,loan_product=loan_product)