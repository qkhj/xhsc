# coding:utf-8

import os

from flask import Module, session, request, render_template, redirect, url_for,flash
from flask.ext.login import current_user
import datetime

from scapp import db
from scapp.config import logger
from scapp.config import PER_PAGE

from scapp.models import SC_Loan_Apply
from scapp.models import SC_Co_Borrower
from scapp.models import SC_Guaranty
from scapp.models import SC_Guarantees
from scapp.models import SC_Classify
from scapp.models import View_Query_Loan
from scapp.logic.total import Property
from scapp.models import SC_UserRole

from scapp import app

from scapp.models import SC_Loan_Product

# 资产分类
@app.route('/Process/zcfl/zcfl', methods=['GET'])
def Process_zcfl():
    loan_product = SC_Loan_Product.query.all()
    return render_template("Process/zcfl/zcfl_search.html",loan_product=loan_product)
# 保存资产质量分类
@app.route('/Process/zcfl/zcfl_save/<int:loan_apply_id>/<int:stiatic>', methods=['POST'])
def zcfl_save(loan_apply_id,stiatic):
    page = request.form['page']
    customer_name = request.form['customer_name']
    loan_type = request.form['loan_type']
    classify = request.form['classify']
    #获取最新资产分类信息
    lastProperty = Property() 
    inform = lastProperty.queryLastProperty(loan_apply_id)
    if inform:
    	is_pass = inform.is_pass
    	index_add = inform.index_add
    	#未审核
    	if is_pass==0:
    		#更新最新状态
    		lastProperty.updateLastProperty(loan_apply_id,index_add,stiatic)
    	#审核通过则新增记录
    	else:
    		lastProperty.addProperty(loan_apply_id,index_add+1,stiatic)
    else:
    	lastProperty.addProperty(loan_apply_id,0,stiatic)
    loan_apply = lastProperty.queryList(customer_name,loan_type,classify,int(page))
    role = SC_UserRole.query.filter_by(user_id=current_user.id).first().role
    
    loan_product = SC_Loan_Product.query.all()
    
    return render_template("Process/zcfl/zcfl.html",loan_apply=loan_apply,customer_name=customer_name,classify=classify,
    	loan_type=loan_type,role=role,page=page,loan_product=loan_product)
# 审核资产质量分类
@app.route('/Process/zcfl/zcfl_save_sh/<int:loan_apply_id>/<int:is_pass>', methods=['POST'])
def zcfl_save_sh(loan_apply_id,is_pass):
    page = request.form['page']
    customer_name = request.form['customer_name']
    loan_type = request.form['loan_type']
    classify = request.form['classify']
    #获取最新资产分类信息
    lastProperty = Property() 
    inform = lastProperty.queryLastProperty(loan_apply_id)
    if inform:
    	index_add = inform.index_add
    	lastProperty.updateLastPropertyBysh(loan_apply_id,index_add,is_pass)
    loan_apply = lastProperty.queryList(customer_name,loan_type,classify,int(page))
    role = SC_UserRole.query.filter_by(user_id=current_user.id).first().role
    
    loan_product = SC_Loan_Product.query.all()
    
    return render_template("Process/zcfl/zcfl.html",loan_apply=loan_apply,customer_name=customer_name,classify=classify,
    	loan_type=loan_type,role=role,page=page,loan_product=loan_product)
# 资产分类搜索
@app.route('/Process/zcfl/zcfl_search/<int:page>', methods=['GET','POST'])
def zcfl_search(page):
    customer_name = request.form['customer_name']
    loan_type = request.form['loan_type']
    classify = request.form['classify']
    propertyList = Property() 
    loan_apply = propertyList.queryList(customer_name,loan_type,classify,page)
    role = SC_UserRole.query.filter_by(user_id=current_user.id).first().role
    
    loan_product = SC_Loan_Product.query.all()
    
    return render_template("Process/zcfl/zcfl.html",loan_apply=loan_apply,customer_name=customer_name,classify=classify,
    	loan_type=loan_type,role=role,page=page,loan_product=loan_product)

	