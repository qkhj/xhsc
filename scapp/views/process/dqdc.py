# coding:utf-8

import os

from flask import Module, session, request, render_template, redirect, url_for,flash,send_from_directory,send_file
from flask.ext.login import current_user
import datetime
import urllib2 

from scapp import db

from scapp.config import logger
from scapp.config import PER_PAGE
from scapp.config import PROCESS_STATUS_DKSQSH
from scapp.config import PROCESS_STATUS_DQDC
from scapp.config import UPLOAD_FOLDER_REL
from scapp.config import UPLOAD_FOLDER_ABS

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
from scapp.models import SC_Credit_Upload

from scapp.models import View_Query_Loan

from scapp import app
from sqlalchemy.sql import or_ 

# 贷前调查
@app.route('/Process/dqdc/dqdc', methods=['GET'])
def Process_dqdc():
    return render_template("Process/dqdc/dqdc_search.html")
	
# 贷款调查——微贷
@app.route('/Process/dqdc/dqdc_search/<int:page>', methods=['GET','POST'])
def dqdc_search(page):
    # 关联查找
    # 打印sql: print db.session.query(SC_Loan_Apply,SC_Apply_Info).join(SC_Apply_Info)
    # loan_apply = db.session.query(SC_Loan_Apply,SC_Apply_Info).join(SC_Apply_Info)
    # loan_apply = SC_Loan_Apply.query.order_by("id").paginate(page, per_page = PER_PAGE)
    customer_name = request.form['customer_name']
    loan_type = request.form['loan_type']
    sql = ""
    if loan_type != '0':
        sql = "loan_type='"+loan_type+"' and "
    sql += " process_status='"+PROCESS_STATUS_DKSQSH+"'"
    sql += " and (A_loan_officer="+str(current_user.id)+" or B_loan_officer="+str(current_user.id)+" or yunying_loan_officer="+str(current_user.id)+")"

    if customer_name:
        sql += " and (company_customer_name like '%"+customer_name+"%' or individual_customer_name like '%"+customer_name+"%')"

    loan_apply = View_Query_Loan.query.filter(sql).paginate(page, per_page = PER_PAGE)
    return render_template("Process/dqdc/dqdc.html",loan_apply=loan_apply,customer_name=customer_name,loan_type=loan_type)

# 贷款调查——微贷信息
@app.route('/Process/dqdc/dqdc_wd/<belong_customer_type>/<int:belong_customer_value>/<int:id>', methods=['GET'])
def dqdc_wd(belong_customer_type,belong_customer_value,id):
    loan_apply = SC_Loan_Apply.query.filter_by(id=id).first()
    return render_template("Process/dqdc/dqdc_wd.html",loan_apply=loan_apply,belong_customer_type=belong_customer_type,
        belong_customer_value=belong_customer_value,id=id)

# 贷款调查——微贷(基本情况)
@app.route('/Process/dqdc/dqdcWd_jbqk/<belong_customer_type>/<int:belong_customer_value>/<int:id>', methods=['GET'])
def dqdcWd_jbqk(belong_customer_type,belong_customer_value,id):
    if belong_customer_type == 'Company':
        customer = SC_Company_Customer.query.filter_by(id=belong_customer_value).first()
    else :
        customer = SC_Individual_Customer.query.filter_by(id=belong_customer_value).first()

    loan_apply = SC_Loan_Apply.query.filter_by(id=id).first()
    apply_info = SC_Apply_Info.query.filter_by(loan_apply_id=id).first()
    loan_purpose = SC_Loan_Purpose.query.order_by("id").all()
    credit_history = SC_Credit_History.query.filter_by(loan_apply_id=id).all()
    co_borrower = SC_Co_Borrower.query.filter_by(loan_apply_id=id).all()
    guaranty = SC_Guaranty.query.filter_by(loan_apply_id=id).all()
    guarantees = SC_Guarantees.query.filter_by(loan_apply_id=id).all()
    riskanalysis_and_findings = SC_Riskanalysis_And_Findings.query.filter_by(loan_apply_id=id).first()

    return render_template("Process/dqdc/dqdcWd_jbqk.html",belong_customer_type=belong_customer_type,
        belong_customer_value=belong_customer_value,id=id,customer=customer,loan_apply=loan_apply,
        apply_info=apply_info,loan_purpose=loan_purpose,credit_history=credit_history,
        co_borrower=co_borrower,guaranty=guaranty,guarantees=guarantees,
        riskanalysis_and_findings=riskanalysis_and_findings)

# 编辑贷款调查——微贷(基本情况)
@app.route('/Process/dqdc/edit_dqdcWd_jbqk/<int:id>', methods=['POST'])
def edit_dqdcWd_jbqk(id):
    try:
        riskanalysis_and_findings = SC_Riskanalysis_And_Findings.query.filter_by(loan_apply_id=id).first()
        if riskanalysis_and_findings:
            riskanalysis_and_findings.analysis_conclusion = request.form['analysis_conclusion']
            riskanalysis_and_findings.amount_recommended = request.form['amount_recommended']
            riskanalysis_and_findings.recommended_deadline = request.form['recommended_deadline']
            riskanalysis_and_findings.recommended_rates = request.form['recommended_rates']
            riskanalysis_and_findings.monthly_repayment_amount = request.form['monthly_repayment_amount']
            riskanalysis_and_findings.recommended_way_of_security = request.form['recommended_way_of_security']
            riskanalysis_and_findings.income_ratio = request.form['income_ratio']
            riskanalysis_and_findings.survey_signature = request.form['survey_signature']
            riskanalysis_and_findings.survey_date = request.form['survey_date']

            verification_list = request.form.getlist('verification')
            riskanalysis_and_findings.verification = 0
            # 循环获取表单
            for i in range(len(verification_list)):
                riskanalysis_and_findings.verification += int(verification_list[i])
            
            riskanalysis_and_findings.others = request.form['others']
            riskanalysis_and_findings.bool_grant = request.form['bool_grant']
            if request.form['bool_grant'] == '1':
                riskanalysis_and_findings.amount = request.form['amount']
                riskanalysis_and_findings.deadline = request.form['deadline']
                riskanalysis_and_findings.rates = request.form['rates']
                riskanalysis_and_findings.monthly_repayment = request.form['monthly_repayment']
                riskanalysis_and_findings.approve_reason = request.form['approve_reason']
            else:
                riskanalysis_and_findings.refuse_reason = request.form['refuse_reason']

            riskanalysis_and_findings.modify_user = current_user.id
            riskanalysis_and_findings.modify_date = datetime.datetime.now()
            
        else:
            verification_list = request.form.getlist('verification')
            verification_value = 0
            # 循环获取表单
            for i in range(len(verification_list)):
                verification_value += int(verification_list[i])

            SC_Riskanalysis_And_Findings(id,request.form['analysis_conclusion'],
                request.form['amount_recommended'],request.form['recommended_deadline'],
                request.form['recommended_rates'],request.form['monthly_repayment_amount'],
                request.form['recommended_way_of_security'],request.form['income_ratio'],
                request.form['survey_signature'],request.form['survey_date'],
                verification_value,request.form['others'],
                request.form['bool_grant'],request.form['amount'],
                request.form['deadline'],request.form['rates'],
                request.form['monthly_repayment'],request.form['approve_reason'],
                request.form['refuse_reason'],request.form['other_deliberations'],
                request.form['positive'],request.form['opposite']).add()


        loan_apply = SC_Loan_Apply.query.filter_by(id=id).first()
        loan_apply.process_status = PROCESS_STATUS_DQDC

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

    return redirect("Process/dqdc/dqdc")

# 贷款调查——小额贷款
@app.route('/Process/dqdc/dqdc_xed/<belong_customer_type>/<int:belong_customer_value>/<int:id>', methods=['GET'])
def dqdc_xed(belong_customer_type,belong_customer_value,id):
    loan_apply = SC_Loan_Apply.query.filter_by(id=id).first()
    return render_template("Process/dqdc/dqdc_xed.html",loan_apply=loan_apply,belong_customer_type=belong_customer_type,
        belong_customer_value=belong_customer_value,id=id)

# 贷款调查——小额贷款(基本情况)
@app.route('/Process/dqdc/dqdcXed_jbqk/<belong_customer_type>/<int:belong_customer_value>/<int:id>', methods=['GET'])
def dqdcXed_jbqk(belong_customer_type,belong_customer_value,id):
    if belong_customer_type == 'Company':
        customer = SC_Company_Customer.query.filter_by(id=belong_customer_value).first()
    else :
        customer = SC_Individual_Customer.query.filter_by(id=belong_customer_value).first()

    loan_apply = SC_Loan_Apply.query.filter_by(id=id).first()
    apply_info = SC_Apply_Info.query.filter_by(loan_apply_id=id).first()
    loan_purpose = SC_Loan_Purpose.query.order_by("id").all()
    credit_history = SC_Credit_History.query.filter_by(loan_apply_id=id).all()
    guarantees_for_others = SC_Guarantees_For_Others.query.filter_by(loan_apply_id=id).all()
    financial_overview = SC_Financial_Overview.query.filter_by(loan_apply_id=id).first()
    non_financial_analysis = SC_Non_Financial_Analysis.query.filter_by(loan_apply_id=id).first()
    riskanalysis_and_findings = SC_Riskanalysis_And_Findings.query.filter_by(loan_apply_id=id).first()
    
    return render_template("Process/dqdc/dqdcXed_jbqk.html",belong_customer_type=belong_customer_type,
        belong_customer_value=belong_customer_value,id=id,customer=customer,loan_apply=loan_apply,
        apply_info=apply_info,loan_purpose=loan_purpose,credit_history=credit_history,
        guarantees_for_others=guarantees_for_others,riskanalysis_and_findings=riskanalysis_and_findings,
        financial_overview=financial_overview,non_financial_analysis=non_financial_analysis)

# 编辑贷款调查——小额贷款(基本情况)
@app.route('/Process/dqdc/edit_dqdcXed_jbqk/<int:id>', methods=['POST'])
def edit_dqdcXed_jbqk(id):
    try:
        financial_overview = SC_Financial_Overview.query.filter_by(loan_apply_id=id).first()
        if financial_overview:
            financial_overview.current_assets = request.form['current_assets']
            financial_overview.current_liabilities = request.form['current_liabilities']
            financial_overview.bank_deposits = request.form['bank_deposits']
            financial_overview.accounts_payable = request.form['accounts_payable']
            financial_overview.accounts_receivable = request.form['accounts_receivable']
            financial_overview.receipts_in_advance = request.form['receipts_in_advance']
            financial_overview.prepayments = request.form['prepayments']
            financial_overview.short_term_borrowings = request.form['short_term_borrowings']
            financial_overview.stock = request.form['stock']
            financial_overview.long_term_borrowings = request.form['long_term_borrowings']
            financial_overview.fixed_assets = request.form['fixed_assets']
            financial_overview.total_liabilities = request.form['total_liabilities']
            financial_overview.other_operating_assets = request.form['other_operating_assets']
            financial_overview.equity = request.form['equity']
            financial_overview.total_assets = request.form['total_assets']
            financial_overview.liabilities_plus_equity = request.form['liabilities_plus_equity']
            financial_overview.other_non_sheet_assets = request.form['other_non_sheet_assets']
            financial_overview.other_non_sheet_liabilities = request.form['other_non_sheet_liabilities']
            financial_overview.average_monthly_turnover = request.form['average_monthly_turnover']
            financial_overview.average_net_profit = request.form['average_net_profit']
            financial_overview.average_monthly_disposable_income = request.form['average_monthly_disposable_income']
            financial_overview.asset_liability_ratio = request.form['asset_liability_ratio']
            financial_overview.current_ratio = request.form['current_ratio']
            financial_overview.quick_ratio = request.form['quick_ratio']
            financial_overview.inventory_turnover_ratio = request.form['inventory_turnover_ratio']
            financial_overview.accounts_receivable_turnover_ratio = request.form['accounts_receivable_turnover_ratio']
            financial_overview.accounts_payable_turnover_ratio = request.form['accounts_payable_turnover_ratio']
            financial_overview.returns_on_capital = request.form['returns_on_capital']
            financial_overview.gross_margin = request.form['gross_margin']
            financial_overview.net_profit_margin = request.form['net_profit_margin']
        else:
            SC_Financial_Overview(id,request.form['current_assets'],request.form['current_liabilities'],
                request.form['bank_deposits'],request.form['accounts_payable'],
                request.form['accounts_receivable'],request.form['receipts_in_advance'],
                request.form['prepayments'],request.form['short_term_borrowings'],
                request.form['stock'],request.form['long_term_borrowings'],
                request.form['fixed_assets'],request.form['total_liabilities'],
                request.form['other_operating_assets'],request.form['equity'],
                request.form['total_assets'],request.form['liabilities_plus_equity'],
                request.form['other_non_sheet_assets'],request.form['other_non_sheet_liabilities'],
                request.form['average_monthly_turnover'],request.form['average_net_profit'],
                request.form['average_monthly_disposable_income'],request.form['asset_liability_ratio'],
                request.form['current_ratio'],request.form['quick_ratio'],
                request.form['inventory_turnover_ratio'],request.form['accounts_receivable_turnover_ratio'],
                request.form['accounts_payable_turnover_ratio'],request.form['returns_on_capital'],
                request.form['gross_margin'],request.form['net_profit_margin']).add()

        non_financial_analysis = SC_Non_Financial_Analysis.query.filter_by(loan_apply_id=id).first()
        if non_financial_analysis:
            non_financial_analysis.operating_history = request.form['operating_history']
            non_financial_analysis.structure_and_market = request.form['structure_and_market']
            non_financial_analysis.finance = request.form['finance']
            non_financial_analysis.changes_in_operations_1 = request.form['changes_in_operations_1']
            non_financial_analysis.changes_in_operations_2 = request.form['changes_in_operations_2']
            non_financial_analysis.investment_1 = request.form['investment_1']
            non_financial_analysis.investment_2 = request.form['investment_2']
            non_financial_analysis.investment_plan_1 = request.form['investment_plan_1']
            non_financial_analysis.investment_plan_2 = request.form['investment_plan_2']
            non_financial_analysis.loan_purpose_detail = request.form['loan_purpose_detail']
            non_financial_analysis.personal_circumstances = request.form['personal_circumstances']
            non_financial_analysis.impression_of_the_customer = request.form['impression_of_the_customer']
            non_financial_analysis.other_sources_of_repayment = request.form['other_sources_of_repayment']
        else:
            SC_Non_Financial_Analysis(id,request.form['operating_history'],
                request.form['structure_and_market'],request.form['finance'],
                request.form['changes_in_operations_1'],request.form['changes_in_operations_2'],
                request.form['investment_1'],request.form['investment_2'],
                request.form['investment_plan_1'],request.form['investment_plan_2'],
                request.form['loan_purpose_detail'],request.form['personal_circumstances'],
                request.form['impression_of_the_customer'],request.form['other_sources_of_repayment']).add()

        riskanalysis_and_findings = SC_Riskanalysis_And_Findings.query.filter_by(loan_apply_id=id).first()
        if riskanalysis_and_findings:
            riskanalysis_and_findings.analysis_conclusion = request.form['analysis_conclusion']
            riskanalysis_and_findings.amount_recommended = request.form['amount_recommended']
            riskanalysis_and_findings.recommended_deadline = request.form['recommended_deadline']
            riskanalysis_and_findings.recommended_rates = request.form['recommended_rates']
            riskanalysis_and_findings.monthly_repayment_amount = request.form['monthly_repayment_amount']
            riskanalysis_and_findings.recommended_way_of_security = request.form['recommended_way_of_security']
            riskanalysis_and_findings.income_ratio = request.form['income_ratio']
            riskanalysis_and_findings.survey_signature = request.form['survey_signature']
            riskanalysis_and_findings.survey_date = request.form['survey_date']

            verification_list = request.form.getlist('verification')
            riskanalysis_and_findings.verification = 0
            # 循环获取表单
            for i in range(len(verification_list)):
                riskanalysis_and_findings.verification += int(verification_list[i])
            
            riskanalysis_and_findings.others = request.form['others']
            riskanalysis_and_findings.bool_grant = request.form['bool_grant']
            if request.form['bool_grant'] == '1':
                riskanalysis_and_findings.amount = request.form['amount']
                riskanalysis_and_findings.deadline = request.form['deadline']
                riskanalysis_and_findings.rates = request.form['rates']
                riskanalysis_and_findings.monthly_repayment = request.form['monthly_repayment']
                riskanalysis_and_findings.approve_reason = request.form['approve_reason']
            else:
                riskanalysis_and_findings.refuse_reason = request.form['refuse_reason']
        else:
            verification_list = request.form.getlist('verification')
            verification_value = 0
            # 循环获取表单
            for i in range(len(verification_list)):
                verification_value += int(verification_list[i])

            SC_Riskanalysis_And_Findings(id,request.form['analysis_conclusion'],
                request.form['amount_recommended'],request.form['recommended_deadline'],
                request.form['recommended_rates'],request.form['monthly_repayment_amount'],
                request.form['recommended_way_of_security'],request.form['income_ratio'],
                request.form['survey_signature'],request.form['survey_date'],
                verification_value,request.form['others'],
                request.form['bool_grant'],request.form['amount'],
                request.form['deadline'],request.form['rates'],
                request.form['monthly_repayment'],request.form['approve_reason'],
                request.form['refuse_reason'],request.form['other_deliberations'],
                request.form['positive'],request.form['opposite']).add()

        loan_apply = SC_Loan_Apply.query.filter_by(id=id).first()
        loan_apply.process_status = PROCESS_STATUS_DQDC

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

    return redirect("Process/dqdc/dqdc")


# 上传征信材料
@app.route('/Process/dqdc/credit_upload/<int:loan_apply_id>', methods=['GET','POST'])
def credit_upload(loan_apply_id):
    if request.method == 'GET':
        credit_upload=SC_Credit_Upload.query.filter_by(loan_apply_id=loan_apply_id).order_by("id").all()
        return render_template("Process/dqdc/credit_upload.html",credit_upload=credit_upload,loan_apply_id=loan_apply_id)
    else:
        try:
            # 先获取上传文件
            f = request.files['attachment']
            fname = f.filename
            if not os.path.exists(os.path.join(UPLOAD_FOLDER_ABS,str(loan_apply_id))):
                os.mkdir(os.path.join(UPLOAD_FOLDER_ABS,str(loan_apply_id)))
            f.save(os.path.join(UPLOAD_FOLDER_ABS,'%d\\%s' % (loan_apply_id,fname)))

            SC_Credit_Upload(loan_apply_id,request.form['info_name'],request.form['info_description'],
                fname).add()

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

        return redirect('Process/dqdc/credit_upload/%d' % loan_apply_id)

# 下载征信材料
@app.route('/Process/dqdc/credit_download/<int:loan_apply_id>/<int:id>', methods=['GET'])
def credit_download(loan_apply_id,id):
    fname = SC_Credit_Upload.query.filter_by(id=id).first().attachment
    #return send_from_directory(app.static_folder, 'upload/%d/%s' % (loan_apply_id,fname))
    return redirect(url_for('static', filename='upload/'+ str(loan_apply_id) + '/' + fname), code=301)

# 下载征信材料
@app.route('/Process/dqdc/credit_delete/<int:loan_apply_id>/<int:id>', methods=['GET'])
def credit_delete(loan_apply_id,id):
    try:
        fname = SC_Credit_Upload.query.filter_by(id=id).first().attachment
        targetFile = os.path.join(UPLOAD_FOLDER_ABS,str(loan_apply_id),fname)
        if os.path.exists(targetFile):
            os.remove(targetFile)

        SC_Credit_Upload.query.filter_by(id=id).delete()

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

    return redirect('Process/dqdc/credit_upload/%d' % loan_apply_id)
    
    