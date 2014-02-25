# coding:utf-8

import os

from flask import Module, session, request, render_template, redirect, url_for,flash
from flask.ext.login import current_user
import datetime

from scapp import db
from scapp.config import logger
from scapp.config import PER_PAGE
from scapp.config import PROCESS_STATUS_SPJY_TG
from scapp.models import View_Query_Loan

from scapp import app

# 贷后管理
@app.route('/Process/dhgl/dhgl', methods=['GET'])
def Process_dhgl():
    return render_template("Process/dhgl/dhgl_search.html")

# 贷后管理搜索
@app.route('/Process/dhgl/dhgl_search/<int:page>', methods=['GET','POST'])
def dhgl_search(page):
	customer_name = request.form['customer_name']
	loan_type = request.form['loan_type']
	sql = ""
	if loan_type != '0':
	    sql = "loan_type='"+loan_type+"' and "
	sql += " process_status='"+PROCESS_STATUS_SPJY_TG+"'"
	sql += " and (A_loan_officer="+str(current_user.id)+" or B_loan_officer="+str(current_user.id)+" or yunying_loan_officer="+str(current_user.id)+")"

	if customer_name:
	    sql += " and (company_customer_name like '%"+customer_name+"%' or individual_customer_name like '%"+customer_name+"%')"

	loan_apply = View_Query_Loan.query.filter(sql).paginate(page, per_page = PER_PAGE)
	return render_template("Process/dhgl/dhgl.html",loan_apply=loan_apply,customer_name=customer_name,loan_type=loan_type)
	
# 贷后管理——贷后管理
@app.route('/Process/dhgl/edit_dhgl/<int:loan_apply_id>', methods=['GET'])
def edit_dhgl(loan_apply_id):
    return render_template("Process/dhgl/edit_dhgl.html")

# 贷后管理——新增标准
@app.route('/Process/dhgl/new_bz', methods=['GET'])
def new_bz():
    return render_template("Process/dhgl/new_bz.html")

# 贷后管理——新增非标准
@app.route('/Process/dhgl/new_fbz', methods=['GET'])
def new_fbz():
    return render_template("Process/dhgl/new_fbz.html")
        
# 贷后管理——管理信息列表
@app.route('/Process/dhgl/glxxlb', methods=['GET'])
def dhgl_glxxlb():
    return render_template("Process/dhgl/glxxlb.html")

# 贷后管理——管理信息
@app.route('/Process/dhgl/glxx', methods=['GET'])
def dhgl_glxx():
    return render_template("Process/dhgl/glxx.html")

# 贷后管理——非标监控说明
@app.route('/Process/dhgl/fbjksm', methods=['GET'])
def dhgl_fbjksm():
    return render_template("Process/dhgl/fbjksm.html")