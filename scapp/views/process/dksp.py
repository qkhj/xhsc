# coding:utf-8

import os

from flask import Module, session, request, render_template, redirect, url_for,flash
from flask.ext.login import current_user
import datetime

from scapp import db

from scapp.config import logger
from scapp.config import PER_PAGE
from scapp.config import PROCESS_STATUS_DQDC
from scapp.config import PROCESS_STATUS_DKSP

from scapp.models import SC_Individual_Customer
from scapp.models import SC_Company_Customer
from scapp.models import SC_User

from scapp.models import SC_Relations
from scapp.models import SC_Manage_Info
from scapp.models import SC_Financial_Affairs

from scapp.models import SC_Relation_Type
from scapp.models import SC_Industry
from scapp.models import SC_Business_Type
from scapp.models import SC_Loan_Purpose

from scapp.models import SC_Loan_Apply
from scapp.models import SC_Apply_Info
from scapp.models import SC_Credit_History
from scapp.models import SC_Co_Borrower
from scapp.models import SC_Guarantees_For_Others
from scapp.models import SC_Guaranty
from scapp.models import SC_Guarantees
#from scapp.models import SC_Financial_Overview
#from scapp.models import SC_Non_Financial_Analysis
from scapp.models import SC_Riskanalysis_And_Findings

from scapp.models import View_Query_Loan

from scapp import app

# 贷款审批
@app.route('/Process/dksp/dksp', methods=['GET'])
def Process_dksp():
    return render_template("Process/dksp/dksp_search.html")
	
# 贷款审批
@app.route('/Process/dksp/dksp_search/<int:page>', methods=['GET','POST'])
def dksp_search(page):
    # 关联查找
    # 打印sql: print db.session.query(SC_Loan_Apply,SC_Apply_Info).join(SC_Apply_Info)
    # loan_apply = db.session.query(SC_Loan_Apply,SC_Apply_Info).join(SC_Apply_Info)
    # loan_apply = SC_Loan_Apply.query.order_by("id").paginate(page, per_page = PER_PAGE)
    customer_name = request.form['customer_name']
    loan_type = request.form['loan_type']
    sql = ""
    if loan_type != '0':
        sql = "loan_type='"+loan_type+"' and "
    sql += " process_status='"+PROCESS_STATUS_DQDC+"'"

    if customer_name:
        sql += " and (company_customer_name like '%"+customer_name+"%' or individual_customer_name like '%"+customer_name+"%')"

    loan_apply = View_Query_Loan.query.filter(sql).paginate(page, per_page = PER_PAGE)
    return render_template("Process/dksp/dksp.html",loan_apply=loan_apply,customer_name=customer_name,loan_type=loan_type)

# 跳转到编辑贷款审批信息
@app.route('/Process/dksp/goto_edit_dksp/<belong_customer_type>/<int:belong_customer_value>/<int:id>', methods=['GET'])
def goto_edit_dksp(belong_customer_type,belong_customer_value,id):
    return render_template("Process/dksp/edit_dksp.html",belong_customer_type=belong_customer_type,
        belong_customer_value=belong_customer_value,id=id)

# 跳转到编辑贷款审批信息
@app.route('/Process/dksp/goto_edit_dksp_info/<belong_customer_type>/<int:belong_customer_value>/<int:id>', methods=['GET'])
def goto_edit_dksp_info(belong_customer_type,belong_customer_value,id):
    
    if belong_customer_type == 'Company':
        customer = SC_Company_Customer.query.filter_by(id=belong_customer_value).first()
    else :
        customer = SC_Individual_Customer.query.filter_by(id=belong_customer_value).first()

    loan_apply = SC_Loan_Apply.query.filter_by(id=id).first()
    loan_purpose = SC_Loan_Purpose.query.order_by("id").all()
    user = SC_User.query.order_by("id").all()
    apply_info = SC_Apply_Info.query.filter_by(loan_apply_id=id).first()
    co_borrower = SC_Co_Borrower.query.filter_by(loan_apply_id=id).all()
    guaranty = SC_Guaranty.query.filter_by(loan_apply_id=id).all()
    guarantees = SC_Guarantees.query.filter_by(loan_apply_id=id).all()
    riskanalysis_and_findings = SC_Riskanalysis_And_Findings.query.filter_by(loan_apply_id=id).first()

    return render_template("Process/dksp/edit_dksp_info.html",
        customer=customer,id=id,loan_apply=loan_apply,loan_purpose=loan_purpose,apply_info=apply_info,
        co_borrower=co_borrower,guaranty=guaranty,guarantees=guarantees,
        riskanalysis_and_findings=riskanalysis_and_findings,user=user)

# 跳转到编辑贷款审批信息
@app.route('/Process/dksp/edit_dksp/<int:loan_apply_id>', methods=['POST'])
def edit_dksp(loan_apply_id):
    try:
        loan_apply = SC_Loan_Apply.query.filter_by(id=loan_apply_id).first()
        loan_apply.examiner_1 = request.form['examiner_1']
        loan_apply.examiner_2 = request.form['examiner_2']
        loan_apply.approver = request.form['approver']
        loan_apply.process_status = PROCESS_STATUS_DKSP

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

    return redirect("Process/dksp/dksp")
