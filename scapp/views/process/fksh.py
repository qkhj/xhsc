# coding:utf-8

import os

from flask import Module, session, request, render_template, redirect, url_for,flash
from flask.ext.login import current_user
import datetime

from scapp import db
from scapp.config import logger
from scapp.config import PER_PAGE
from scapp.config import PROCESS_STATUS_DKFKJH
from scapp.config import PROCESS_STATUS_SPJY

from scapp.models import SC_Loan_Apply
from scapp.models import SC_Apply_Info
from scapp.models import SC_Riskanalysis_And_Findings
from scapp.models import SC_Approval_Decision
from scapp.models import SC_Co_Borrower
from scapp.models import SC_Guaranty
from scapp.models import SC_Guarantees
from scapp.models.repayment.sc_repayment_plan import SC_Repayment_Plan
from scapp.models.repayment.sc_repayment_plan_detail import SC_Repayment_plan_detail

from scapp.models import View_Query_Loan

from scapp import app
from sqlalchemy.sql import or_ 

# 放款审核
@app.route('/Process/fksh/fksh', methods=['GET'])
def Process_fksh():
    return render_template("Process/fksh/fksh_search.html")
	
# 放款审核
@app.route('/Process/fksh/fksh_search/<int:page>', methods=['GET','POST'])
def fksh_search(page):
    # 关联查找
    # 打印sql: print db.session.query(SC_Loan_Apply,SC_Apply_Info).join(SC_Apply_Info)
    # loan_apply = db.session.query(SC_Loan_Apply,SC_Apply_Info).join(SC_Apply_Info)
    # loan_apply = SC_Loan_Apply.query.order_by("id").paginate(page, per_page = PER_PAGE)
    loan_apply = View_Query_Loan.query.filter('process_status=:process_status',
        or_('examiner_1=:examiner_1','examiner_2=:examiner_2','approver=:approver')).params(
        process_status=PROCESS_STATUS_DKFKJH,examiner_1=current_user.id,examiner_2=current_user.id,
        approver=current_user.id).paginate(page, per_page = PER_PAGE)
    return render_template("Process/fksh/fksh.html",loan_apply=loan_apply)

# 放款审核——跳转到放款审核(放款信息)
@app.route('/Process/fksh/goto_edit_fksh/<int:id>', methods=['GET'])
def goto_edit_fksh(id):
    loan_apply = SC_Loan_Apply.query.filter_by(id=id).first()
    return render_template("Process/fksh/edit_fksh.html",id=id,loan_apply=loan_apply)

# 审贷会决议单
@app.route('/Process/fksh/edit_sdhjyd/<int:loan_apply_id>', methods=['GET'])
def edit_sdhjyd(loan_apply_id):
    riskanalysis_and_findings = SC_Riskanalysis_And_Findings.query.filter_by(loan_apply_id=loan_apply_id).first()
    approval_decision = SC_Approval_Decision.query.filter_by(loan_apply_id=loan_apply_id).first()
    co_borrower = SC_Co_Borrower.query.filter_by(loan_apply_id=loan_apply_id).all()
    guaranty = SC_Guaranty.query.filter_by(loan_apply_id=loan_apply_id).all()
    guaranty = SC_Guaranty.query.filter_by(loan_apply_id=loan_apply_id).all()
    guarantees = SC_Guarantees.query.filter_by(loan_apply_id=loan_apply_id).all()
    return render_template("Process/fksh/edit_sdhjyd.html",loan_apply_id=loan_apply_id,
        riskanalysis_and_findings=riskanalysis_and_findings,
        approval_decision=approval_decision,co_borrower=co_borrower,guaranty=guaranty
        ,guarantees=guarantees)

# 等额本息还款计划
@app.route('/Process/fksh/edit_debxhkjh/<int:loan_apply_id>', methods=['GET'])
def edit_debxhkjh(loan_apply_id):
    loan_apply = SC_Loan_Apply.query.filter_by(id=loan_apply_id).first()
    apply_info = SC_Apply_Info.query.filter_by(loan_apply_id=loan_apply_id).first()
    repayment_plan_detail = SC_Repayment_plan_detail.query.filter_by(loan_apply_id=loan_apply_id,change_record=1).order_by("id").all()
    return render_template("Process/fksh/edit_debxhkjh.html",loan_apply=loan_apply,apply_info=apply_info,
        repayment_plan_detail=repayment_plan_detail)

# 放款审核——编辑放款审核(放款信息)
@app.route('/Process/fksh/edit_fksh/<int:loan_apply_id>', methods=['POST'])
def edit_fksh(loan_apply_id):
    try:
        approval_decision = SC_Approval_Decision.query.filter_by(loan_apply_id=loan_apply_id).first()
        if approval_decision:
            approval_decision.other_deliberations = request.form['other_deliberations']
            approval_decision.positive = request.form['positive']
            approval_decision.opposite = request.form['opposite']
            approval_decision.bool_grant = request.form['bool_grant']
            approval_decision.amount = request.form['amount']
            approval_decision.deadline = request.form['deadline']
            approval_decision.rates = request.form['rates']
            approval_decision.repayment_type = request.form['repayment_type']
            approval_decision.monthly_repayment = request.form['monthly_repayment']
            approval_decision.bool_co_borrower = request.form['bool_co_borrower']
            approval_decision.bool_guaranty = request.form['bool_guaranty']
            approval_decision.bool_guarantees = request.form['bool_guarantees']
            approval_decision.other_resolution = request.form['other_resolution']
            approval_decision.refuse_reason = request.form['refuse_reason']

            approval_decision.modify_user = current_user.id
            approval_decision.modify_date = datetime.datetime.now()
            
        else:
            SC_Approval_Decision(loan_apply_id,request.form['other_deliberations'],request.form['positive'],
                request.form['opposite'],request.form['bool_grant'],request.form['amount'],request.form['deadline'],
                request.form['rates'],request.form['repayment_type'],request.form['monthly_repayment'],
                request.form['bool_co_borrower'],request.form['bool_guaranty'],request.form['bool_guarantees'],
                request.form['other_resolution'],request.form['refuse_reason']).add()

        loan_apply = SC_Loan_Apply.query.filter_by(id=id).first()
        loan_apply.process_status = PROCESS_STATUS_SPJY

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
        
    return redirect("Process/fksh/fksh") 

# 打印审贷会决议单
@app.route('/Process/fksh/dy_sdhjyd', methods=['GET'])
def dy_sdhjyd():
    return render_template("Process/fksh/dy_sdhjyd.html")
    