# coding:utf-8

import os

from flask import Module, session, request, render_template, redirect, url_for,flash
from flask.ext.login import current_user
import datetime

from scapp import db
from scapp.config import logger
from scapp.config import PER_PAGE
from scapp.config import PROCESS_STATUS_DKSP
from scapp.config import PROCESS_STATUS_DKFKJH

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
from scapp.models import SC_Financial_Overview
from scapp.models import SC_Non_Financial_Analysis
from scapp.models import SC_Riskanalysis_And_Findings
from scapp.models.repayment.sc_repayment_plan import SC_Repayment_Plan
from scapp.models.repayment.sc_repayment_plan_detail import SC_Repayment_plan_detail

from scapp.models import View_Query_Loan

from scapp import app

# 贷款放款
@app.route('/Process/dkfk/dkfk', methods=['GET'])
def Process_dkfk():
    return render_template("Process/dkfk/dkfk_search.html")
	
# 贷款放款——编辑放款
@app.route('/Process/dkfk/dkfk_search/<int:page>', methods=['GET','POST'])
def dkfk_search(page):
    # 关联查找
    # 打印sql: print db.session.query(SC_Loan_Apply,SC_Apply_Info).join(SC_Apply_Info)
    # loan_apply = db.session.query(SC_Loan_Apply,SC_Apply_Info).join(SC_Apply_Info)
    # loan_apply = SC_Loan_Apply.query.order_by("id").paginate(page, per_page = PER_PAGE)
    loan_apply = View_Query_Loan.query.filter('process_status=:process_status').params(process_status=PROCESS_STATUS_DKSP).paginate(page, per_page = PER_PAGE)
    return render_template("Process/dkfk/dkfk.html",loan_apply=loan_apply)

# 贷款放款——跳转到编辑放款(放款信息)
@app.route('/Process/dkfk/goto_edit_dkfk/<int:id>', methods=['GET'])
def goto_edit_dkfk(id):
    loan_apply = SC_Loan_Apply.query.filter_by(id=id).first()
    apply_info = SC_Apply_Info.query.filter_by(loan_apply_id=id).first()
    repayment_plan_detail = SC_Repayment_plan_detail.query.filter_by(loan_apply_id=id,change_record=1).order_by("id").all()
    return render_template("Process/dkfk/edit_dkfk.html",id=id,loan_apply=loan_apply,apply_info=apply_info,
        repayment_plan_detail=repayment_plan_detail)

# 贷款放款——编辑放款(放款信息)
@app.route('/Process/dkfk/edit_dkfk/<int:id>', methods=['POST'])
def edit_dkfk(id):
    try:
        #保存申请信息
        apply_info = SC_Apply_Info.query.filter_by(loan_apply_id=id).first()
        apply_info.repayment_type = request.form['repayment_type']
        apply_info.annual_interest_rate = request.form['annual_interest_rate']
        apply_info.loan_date = request.form['loan_date']
        apply_info.first_repayment_date = request.form['first_repayment_date']
        apply_info.loan_deadline = request.form['loan_deadline']
        apply_info.modify_user=current_user.id
        apply_info.modify_date=datetime.datetime.now()

        #保存还款计划
        repayment_plan_id = 0
        repayment_plan = SC_Repayment_Plan.query.filter_by(loan_apply_id=id).first()
        if repayment_plan:
            repayment_plan_id = repayment_plan.id
            repayment_plan.repayment_type=request.form['repayment_type']
            repayment_plan.amount=request.form['loan_amount_num']
            repayment_plan.lending_date=request.form['loan_date']
            repayment_plan.first_repayment_date=request.form['first_repayment_date']
            repayment_plan.ratio=request.form['annual_interest_rate']
            repayment_plan.installmenst=request.form['loan_deadline']
            repayment_plan.modify_user=current_user.id
            repayment_plan.modify_date=datetime.datetime.now()
        else:
            repayment_plan_new = SC_Repayment_Plan(id,request.form['repayment_type'],request.form['loan_amount_num'],
                request.form['first_repayment_date'],request.form['loan_date'],request.form['annual_interest_rate'],
                request.form['loan_deadline'])
            repayment_plan_new.add()
            db.session.flush()
            repayment_plan_id = repayment_plan_new.id

        #保存还款细则
        SC_Repayment_plan_detail.query.filter_by(loan_apply_id=id,change_record=1).delete()
        db.session.flush()
        for i in range(1,int(request.form['loan_deadline'])+1):
            print i 
            SC_Repayment_plan_detail(repayment_plan_id,id,None,request.form['annual_interest_rate'],
                request.form['mybj%d' % i],request.form['mylx%d' % i],
                request.form['mybx%d' % i],i,request.form['myrq%d' % i],None,1).add() 

        loan_apply = SC_Loan_Apply.query.filter_by(id=id).first()
        loan_apply.process_status = PROCESS_STATUS_DKFKJH

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
        
    return redirect("Process/dkfk/dkfk")

# 贷款放款——编辑放款(放款信息)
@app.route('/Process/dkfk/fkxx', methods=['GET'])
def dkfk_fkxx():
    return render_template("Process/dkfk/fkxx.html")

# 贷款放款——编辑放款(还款计划)
@app.route('/Process/dkfk/hkjh', methods=['GET'])
def dkfk_hkjh():
    return render_template("Process/dkfk/hkjh.html")