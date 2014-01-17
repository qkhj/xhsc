# coding:utf-8

import os

from flask import Module, session, request, render_template, redirect, url_for,flash
from flask.ext.login import current_user
import datetime

from scapp import db
from scapp.config import logger
from scapp.config import PER_PAGE
from scapp.config import PROCESS_STATUS_DKSQ

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

from scapp.models import View_Query_Loan

from scapp import app

# 贷款申请
@app.route('/Process/dksq/dksq', methods=['GET'])
def Process_dksq():
    return render_template("Process/dksq/dksq_search.html")
	
# 贷款申请
@app.route('/Process/dksq/dksq_search/<int:page>', methods=['GET','POST'])
def dksq_search(page):
    # 关联查找
    # 打印sql: print db.session.query(SC_Loan_Apply,SC_Apply_Info).join(SC_Apply_Info)
    # loan_apply = db.session.query(SC_Loan_Apply,SC_Apply_Info).join(SC_Apply_Info)
    # loan_apply = SC_Loan_Apply.query.order_by("id").paginate(page, per_page = PER_PAGE)
    loan_apply = View_Query_Loan.query.filter('marketing_loan_officer=:marketing_loan_officer',
        'process_status=:process_status').params(marketing_loan_officer=current_user.id,
        process_status=PROCESS_STATUS_DKSQ).paginate(page, per_page = PER_PAGE)
    return render_template("Process/dksq/dksq.html",loan_apply=loan_apply)

# 跳转到新增贷款申请
@app.route('/Process/dksq/goto_new_dksq/<belong_customer_type>/<int:page>', methods=['GET'])
def goto_new_dksq(belong_customer_type,page):
    if belong_customer_type == 'Company':
        customer = SC_Company_Customer.query.order_by("id").paginate(page, per_page = PER_PAGE)
        return render_template("Process/dksq/new_dksq.html",belong_customer_type=belong_customer_type,
            customer=customer)
    else :
        customer = SC_Individual_Customer.query.order_by("id").paginate(page, per_page = PER_PAGE)
        return render_template("Process/dksq/new_dksq.html",belong_customer_type=belong_customer_type,
            customer=customer)

# 获取贷款申请基本信息
@app.route('/Process/dksq/goto_new_dksq_info/<belong_customer_type>/<int:belong_customer_value>', methods=['GET'])
def goto_new_dksq_info(belong_customer_type,belong_customer_value):
    if belong_customer_type == 'Company':
        customer = SC_Company_Customer.query.filter_by(id=belong_customer_value).first()
    else :
        customer = SC_Individual_Customer.query.filter_by(id=belong_customer_value).first()

    manager_info = SC_Manage_Info.query.filter_by(belong_customer_type=belong_customer_type,
        belong_customer_value=belong_customer_value).first()
    financial_affairs = SC_Financial_Affairs.query.filter_by(belong_customer_type=belong_customer_type,
        belong_customer_value=belong_customer_value).first()
    loan_purpose = SC_Loan_Purpose.query.order_by("id").all()

    return render_template("Process/dksq/new_dksq_info.html",belong_customer_type=belong_customer_type,
        customer=customer,manager_info=manager_info,financial_affairs=financial_affairs,
        loan_purpose=loan_purpose)

# 新增贷款申请信息
@app.route('/Process/dksq/new_dksq/<belong_customer_type>/<int:belong_customer_value>', methods=['POST'])
def new_dksq(belong_customer_type,belong_customer_value):
    try:
        #生成贷款申请表
        loan_apply = SC_Loan_Apply(request.form['loan_type'],belong_customer_type,belong_customer_value,request.form['customer_name'],request.form['evaluation'],
            current_user.id,None,None,None,'',None,None,None,PROCESS_STATUS_DKSQ,0)
        loan_apply.add()

        #清理缓存
        db.session.flush()

        #保存申请信息
        SC_Apply_Info(loan_apply.id,request.form['loan_amount_num'],request.form['loan_deadline'],
            request.form['month_repayment'],request.form['loan_purpose'],request.form['details'],
            request.form['repayment_source']).add()

        #保存信贷历史
        financing_sources_list = request.form.getlist('financing_sources')
        loan_amount_list = request.form.getlist('loan_amount')
        deadline_list = request.form.getlist('deadline')
        use_list = request.form.getlist('use')
        release_date_list = request.form.getlist('release_date')
        overage_list = request.form.getlist('overage')
        guarantee_list = request.form.getlist('guarantee')
        late_information_list = request.form.getlist('late_information')
        # 循环获取表单
        for i in range(len(financing_sources_list)):
            SC_Credit_History(loan_apply.id,financing_sources_list[i],loan_amount_list[i],
                deadline_list[i],use_list[i],release_date_list[i],
                overage_list[i],guarantee_list[i],late_information_list[i]).add()

        #保存共同借款人
        name_list = request.form.getlist('name')
        relationship_list = request.form.getlist('relationship')
        id_number_list = request.form.getlist('id_number')
        phone_list = request.form.getlist('phone')
        main_business_list = request.form.getlist('main_business')
        address_list = request.form.getlist('address')
        major_assets_list = request.form.getlist('major_assets')
        monthly_income_list = request.form.getlist('monthly_income')
        # 循环获取表单
        for i in range(len(name_list)):
            SC_Co_Borrower(loan_apply.id,name_list[i],relationship_list[i],
                id_number_list[i],phone_list[i],main_business_list[i],
                address_list[i],major_assets_list[i],monthly_income_list[i]).add()

        #保存是否为他人担保
        bank_list = request.form.getlist('bank')
        guarantor_list = request.form.getlist('guarantor')
        guarantee_amount_list = request.form.getlist('guarantee_amount')
        # 循环获取表单
        for i in range(len(bank_list)):
            SC_Guarantees_For_Others(loan_apply.id,bank_list[i],guarantor_list[i],
                guarantee_amount_list[i]).add()

        #保存有无抵押物
        obj_name_list = request.form.getlist('obj_name')
        owner_address_list = request.form.getlist('owner_address')
        description_list = request.form.getlist('description')
        registration_number_list = request.form.getlist('registration_number')
        appraisal_list = request.form.getlist('appraisal')
        mortgage_list = request.form.getlist('mortgage')
        # 循环获取表单
        for i in range(len(obj_name_list)):
            SC_Guaranty(loan_apply.id,obj_name_list[i],owner_address_list[i],
                description_list[i],registration_number_list[i],appraisal_list[i],
                mortgage_list[i],0).add()

        #保存担保信息
        name_db_list = request.form.getlist('name_db')
        address_db_list = request.form.getlist('address_db')
        id_number_db_list = request.form.getlist('id_number_db')
        workunit_db_list = request.form.getlist('workunit_db')
        phone_db_list = request.form.getlist('phone_db')
        relationship_db_list = request.form.getlist('relationship_db')
        # 循环获取表单
        for i in range(len(name_db_list)):
            SC_Guarantees(loan_apply.id,name_db_list[i],address_db_list[i],
                id_number_db_list[i],workunit_db_list[i],phone_db_list[i],
                relationship_db_list[i]).add()

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

    return redirect('Process/dksq/dksq')

# 跳转到编辑贷款申请信息
@app.route('/Process/dksq/goto_edit_dksq/<belong_customer_type>/<int:belong_customer_value>/<int:id>', methods=['GET'])
def goto_edit_dksq(belong_customer_type,belong_customer_value,id):
    return render_template("Process/dksq/edit_dksq.html",belong_customer_type=belong_customer_type,
        belong_customer_value=belong_customer_value,id=id)

# 跳转到编辑贷款申请信息
@app.route('/Process/dksq/goto_edit_dksq_info/<belong_customer_type>/<int:belong_customer_value>/<int:id>', methods=['GET'])
def goto_edit_dksq_info(belong_customer_type,belong_customer_value,id):
    if belong_customer_type == 'Company':
        customer = SC_Company_Customer.query.filter_by(id=belong_customer_value).first()
    else :
        customer = SC_Individual_Customer.query.filter_by(id=belong_customer_value).first()

    loan_apply = SC_Loan_Apply.query.filter_by(id=id).first()
    manager_info = SC_Manage_Info.query.filter_by(belong_customer_type=belong_customer_type,
        belong_customer_value=belong_customer_value).first()
    financial_affairs = SC_Financial_Affairs.query.filter_by(belong_customer_type=belong_customer_type,
        belong_customer_value=belong_customer_value).first()
    loan_purpose = SC_Loan_Purpose.query.order_by("id").all()
    apply_info = SC_Apply_Info.query.filter_by(loan_apply_id=id).first()
    credit_history = SC_Credit_History.query.filter_by(loan_apply_id=id).all()
    co_borrower = SC_Co_Borrower.query.filter_by(loan_apply_id=id).all()
    guarantees_for_others = SC_Guarantees_For_Others.query.filter_by(loan_apply_id=id).all()
    guaranty = SC_Guaranty.query.filter_by(loan_apply_id=id).all()
    guarantees = SC_Guarantees.query.filter_by(loan_apply_id=id).all()

    return render_template("Process/dksq/edit_dksq_info.html",belong_customer_type=belong_customer_type,belong_customer_value=belong_customer_value,
        customer=customer,loan_apply=loan_apply,manager_info=manager_info,financial_affairs=financial_affairs,
        loan_purpose=loan_purpose,apply_info=apply_info,credit_history=credit_history
        ,co_borrower=co_borrower,guarantees_for_others=guarantees_for_others,guaranty=guaranty
        ,guarantees=guarantees)

# 编辑贷款申请信息
@app.route('/Process/dksq/edit_dksq/<int:id>', methods=['POST'])
def edit_dksq(id):

    try:
        #保存贷款申请表
        SC_Loan_Apply.query.filter_by(id=id).update({"loan_type":request.form['loan_type'],
            "evaluation":request.form['evaluation'],"marketing_loan_officer":current_user.id,
            "modify_user":current_user.id,"modify_date":datetime.datetime.now()})

        #保存申请信息
        SC_Apply_Info.query.filter_by(loan_apply_id=id).update({"loan_amount_num":request.form['loan_amount_num'],
            "loan_deadline":request.form['loan_deadline'],"month_repayment":request.form['month_repayment'],
            "loan_purpose":request.form['loan_purpose'],"details":request.form['details'],
            "repayment_source":request.form['repayment_source']})

        #保存信贷历史
        SC_Credit_History.query.filter_by(loan_apply_id=id).delete()
        db.session.flush()

        financing_sources_list = request.form.getlist('financing_sources')
        loan_amount_list = request.form.getlist('loan_amount')
        deadline_list = request.form.getlist('deadline')
        use_list = request.form.getlist('use')
        release_date_list = request.form.getlist('release_date')
        overage_list = request.form.getlist('overage')
        guarantee_list = request.form.getlist('guarantee')
        late_information_list = request.form.getlist('late_information')
        # 循环获取表单
        for i in range(len(financing_sources_list)):
            SC_Credit_History(id,financing_sources_list[i],loan_amount_list[i],
                deadline_list[i],use_list[i],release_date_list[i],
                overage_list[i],guarantee_list[i],late_information_list[i]).add()

        #保存共同借款人
        SC_Co_Borrower.query.filter_by(loan_apply_id=id).delete()
        db.session.flush()

        name_list = request.form.getlist('name')
        relationship_list = request.form.getlist('relationship')
        id_number_list = request.form.getlist('id_number')
        phone_list = request.form.getlist('phone')
        main_business_list = request.form.getlist('main_business')
        address_list = request.form.getlist('address')
        major_assets_list = request.form.getlist('major_assets')
        monthly_income_list = request.form.getlist('monthly_income')
        # 循环获取表单
        for i in range(len(name_list)):
            SC_Co_Borrower(id,name_list[i],relationship_list[i],
                id_number_list[i],phone_list[i],main_business_list[i],
                address_list[i],major_assets_list[i],monthly_income_list[i]).add()

        #保存是否为他人担保
        SC_Guarantees_For_Others.query.filter_by(loan_apply_id=id).delete()
        db.session.flush()

        bank_list = request.form.getlist('bank')
        guarantor_list = request.form.getlist('guarantor')
        guarantee_amount_list = request.form.getlist('guarantee_amount')
        # 循环获取表单
        for i in range(len(bank_list)):
            SC_Guarantees_For_Others(id,bank_list[i],guarantor_list[i],
                guarantee_amount_list[i]).add()

        #保存有无抵押物
        SC_Guaranty.query.filter_by(loan_apply_id=id).delete()
        db.session.flush()

        obj_name_list = request.form.getlist('obj_name')
        owner_address_list = request.form.getlist('owner_address')
        description_list = request.form.getlist('description')
        registration_number_list = request.form.getlist('registration_number')
        appraisal_list = request.form.getlist('appraisal')
        mortgage_list = request.form.getlist('mortgage')
        # 循环获取表单
        for i in range(len(obj_name_list)):
            SC_Guaranty(id,obj_name_list[i],owner_address_list[i],
                description_list[i],registration_number_list[i],appraisal_list[i],
                mortgage_list[i],0).add()

        #保存担保信息
        SC_Guarantees.query.filter_by(loan_apply_id=id).delete()
        db.session.flush()
        
        name_db_list = request.form.getlist('name_db')
        address_db_list = request.form.getlist('address_db')
        id_number_db_list = request.form.getlist('id_number_db')
        workunit_db_list = request.form.getlist('workunit_db')
        phone_db_list = request.form.getlist('phone_db')
        relationship_db_list = request.form.getlist('relationship_db')
        # 循环获取表单
        for i in range(len(name_db_list)):
            SC_Guarantees(id,name_db_list[i],address_db_list[i],
                id_number_db_list[i],workunit_db_list[i],phone_db_list[i],
                relationship_db_list[i]).add()

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

    return redirect('Process/dksq/dksq')