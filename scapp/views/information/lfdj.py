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
from scapp.models import SC_Business_Type
from scapp.models import SC_Loan_Purpose
from scapp.models import SC_Target_Customer

from scapp.models import View_Get_Cus_Mgr

from scapp import app

# 来访登记
@app.route('/Information/lfdj/lfdj', methods=['GET'])
def Information_lfdj():
    user = View_Get_Cus_Mgr.query.filter("role_level>=2").order_by("id").all()#客户经理
    role = SC_UserRole.query.filter_by(user_id=current_user.id).first().role
    return render_template("Information/lfdj/lfdj_search.html",user=user,role=role)
	
# 来访登记
@app.route('/Information/lfdj/lfdj_search/<int:page>', methods=['GET','POST'])
def lfdj_search(page):
    #模糊查询
    manager = request.form['manager']
    customer_name = request.form['customer_name']
    beg_date = request.form['beg_date'] + " 00:00:00"
    end_date = request.form['end_date'] + " 23:59:59"

    sql = " 1=1"
    if manager != '0':
        sql += " and receiver="+manager
    sql += " and create_date between '"+beg_date+"' and '"+end_date + "' "
    if customer_name:
        sql += " and (customer_name like '%"+customer_name+"%' or shop_name like '%"+customer_name+"%') "

    target_customer = SC_Target_Customer.query.filter(sql).order_by("id").paginate(page, per_page = PER_PAGE)

    return render_template("Information/lfdj/lfdj.html",target_customer=target_customer,manager=manager,
        customer_name=customer_name,beg_date=request.form['beg_date'],end_date=request.form['end_date'])

# 新增来访登记
@app.route('/Information/lfdj/new_lfdj', methods=['GET','POST'])
def new_lfdj():
    if request.method == 'POST' :
        try:
            reception_type = request.form['reception_type']

            yingxiao_status = request.form['yingxiao_status']
            client_status = request.form['client_status']
            is_apply_form = request.form['is_apply_form']
            is_have_account = request.form['is_have_account']

            customer_name = request.form['customer_name']
            mobile = request.form['mobile']
            sex = request.form['sex']
            age = request.form['age']
            address = request.form['address']
            industry = request.form['industry']
            business_content = request.form['business_content']

            if reception_type == '2':
                shop_name = request.form['shop_name']
                period = request.form['period']
                property_scope = request.form['property_scope']
                monthly_sales = request.form['monthly_sales']
                employees = request.form['employees']
                business_type = request.form['business_type']
            else:
                shop_name = ''
                period = ''
                property_scope = ''
                monthly_sales = ''
                employees = ''
                business_type = None

            is_need_loan = request.form['is_need_loan']
            if is_need_loan == '1':
                loan_purpose = request.form['loan_purpose']
                loan_amount = request.form['loan_amount']
                repayment_type = request.form['repayment_type']
                guarantee_type = request.form['guarantee_type']
                house_property = request.form['house_property']
                loan_attention = request.form['loan_attention']
                is_have_loan = request.form['is_have_loan']
                is_known_xhnsh = request.form['is_known_xhnsh']
                if is_known_xhnsh == '1':
                    business_with_xhnsh = request.form['business_with_xhnsh']
                else:
                    business_with_xhnsh = ''
                
            else:
                loan_purpose = None
                loan_amount = ''
                repayment_type = ''
                guarantee_type = ''
                house_property = ''
                loan_attention = None
                is_have_loan = None
                is_known_xhnsh = None
                business_with_xhnsh = ''
            is_need_service = request.form['is_need_service']

            SC_Target_Customer(current_user.id,reception_type,
                yingxiao_status,client_status,is_apply_form,is_have_account,
                customer_name,mobile,sex,age,address,
                industry,business_content,shop_name,period,property_scope,monthly_sales,employees,
                business_type,is_need_loan,loan_purpose,loan_amount,repayment_type,guarantee_type,
                house_property,loan_attention,is_have_loan,is_known_xhnsh,business_with_xhnsh,
                is_need_service,0,None,None,None,0).add()

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

        return redirect('Information/lfdj/lfdj')
    else :
        industry = SC_Industry.query.order_by("id").all()
        business_type = SC_Business_Type.query.order_by("id").all()
        loan_purpose = SC_Loan_Purpose.query.order_by("id").all()

        return render_template("Information/lfdj/new_lfdj.html",industry=industry,
            business_type=business_type,loan_purpose=loan_purpose)

# 编辑来访登记
@app.route('/Information/lfdj/edit_lfdj/<int:id>', methods=['GET','POST'])
def edit_lfdj(id):
    if request.method == 'POST' :
        try:
            target_customer = SC_Target_Customer.query.filter_by(id=id).first()

            target_customer.receiver = current_user.id
            target_customer.reception_type = request.form['reception_type']

            target_customer.yingxiao_status = request.form['yingxiao_status']
            target_customer.client_status = request.form['client_status']
            target_customer.is_apply_form = request.form['is_apply_form']
            target_customer.is_have_account = request.form['is_have_account']
            
            target_customer.customer_name = request.form['customer_name']
            target_customer.mobile = request.form['mobile']
            target_customer.sex = request.form['sex']
            target_customer.age = request.form['age']
            target_customer.address = request.form['address']
            target_customer.industry = request.form['industry']
            target_customer.business_content = request.form['business_content']

            if request.form['reception_type'] == '2':
                target_customer.shop_name = request.form['shop_name']
                target_customer.period = request.form['period']
                target_customer.property_scope = request.form['property_scope']
                target_customer.monthly_sales = request.form['monthly_sales']
                target_customer.employees = request.form['employees']
                target_customer.business_type = request.form['business_type']
            else:
                target_customer.shop_name = ''
                target_customer.period = ''
                target_customer.property_scope = ''
                target_customer.monthly_sales = ''
                target_customer.employees = ''
                target_customer.regisiter_type = None

            target_customer.is_need_loan = request.form['is_need_loan']

            if request.form['is_need_loan'] == '1':
                target_customer.loan_purpose = request.form['loan_purpose']
                target_customer.loan_amount = request.form['loan_amount']
                target_customer.repayment_type = request.form['repayment_type']
                target_customer.guarantee_type = request.form['guarantee_type']
                target_customer.house_property = request.form['house_property']
                target_customer.loan_attention = request.form['loan_attention']
                target_customer.is_have_loan = request.form['is_have_loan']
                target_customer.is_known_xhnsh = request.form['is_known_xhnsh']
                if request.form['is_known_xhnsh'] == '1':
                    target_customer.business_with_xhnsh = request.form['business_with_xhnsh']
                else:
                    target_customer.business_with_xhnsh = ''
                
            else:
                target_customer.loan_purpose = None
                target_customer.loan_amount = ''
                target_customer.repayment_type = ''
                target_customer.guarantee_type = ''
                target_customer.house_property = ''
                target_customer.loan_attention = None
                target_customer.is_have_loan = None
                target_customer.is_known_xhnsh = None
                target_customer.business_with_xhnsh = ''
                
            target_customer.is_need_service = request.form['is_need_service']

            target_customer.modify_user = current_user.id
            target_customer.modify_date = datetime.datetime.now()
            
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

        return redirect('Information/lfdj/lfdj')
    else :
        target_customer = SC_Target_Customer.query.filter_by(id=id).first()
        industry = SC_Industry.query.order_by("id").all()
        business_type = SC_Business_Type.query.order_by("id").all()
        loan_purpose = SC_Loan_Purpose.query.order_by("id").all()
        return render_template("Information/lfdj/edit_lfdj.html",target_customer=target_customer,
            industry=industry,business_type=business_type,loan_purpose=loan_purpose)