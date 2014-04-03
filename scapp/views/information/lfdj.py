# coding:utf-8

import os

from flask import Module, session, request, render_template, redirect, url_for,flash
from flask.ext.login import current_user
from sqlalchemy.sql import or_ 
import datetime,time,xlwt,re

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

from scapp.tools.export_excel import export_excel
#from scapp.views.information.lfdj_dic import my_dic
from scapp import app
import json
ezxf=xlwt.easyxf #样式转换

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

# 来访登记
@app.route('/Information/lfdj/export_lfdj', methods=['GET','POST'])
def export_lfdj():
    #模糊查询
    manager = request.form['manager']
    customer_name = request.form['customer_name']
    beg_date = request.form['beg_date'] + " 00:00:00"
    end_date = request.form['end_date'] + " 23:59:59"

    sql = "SELECT sc_user.real_name,"
    sql += "(case reception_type when '1' then '咨询' when '2' then '扫街' end)reception_type ,sc_target_customer.create_date,"
    sql += "(case yingxiao_status when 1 then '已营销' when 0 then '未营销' end)yingxiao_status,"
    sql += "(case client_status when 1 then '现在有需求' when 2 then '态度良好无需求拒绝' when 3 then '态度恶劣拒绝' when 4 then '以后会有需求并填回执' when 5 then '以后有需求未填回执' "
    sql += "when 6 then '有需求但不符要求-年龄不符合要求' when 7 then '有需求但不符要求-经营年限不足一年' when 8 then '有需求但不符要求-外地人在本地居住低于两年' when 9 then '有需求但不符要求-家属不同意' "
    sql += "when 10 then '有需求但不符要求-有不良嗜号' when 11 then '有需求但不符要求-其他' end)client_status,"
    sql += "(case is_apply_form when 1 then '已申请' when 0 then '未申请' end)is_apply_form,"
    sql += "remark,customer_name,sc_target_customer.mobile,"
    sql += "(case sc_target_customer.sex when 1 then '男' when 0 then '女' end)sex,"
    sql += "sc_target_customer.age,address,sc_industry.type_name as industry,business_content,shop_name,period, "
    sql += "property_scope,monthly_sales,employees,sc_business_type.type_name as business_type,is_need_loan,sc_loan_purpose.type_name as loan_purpose,loan_amount, "
    sql += "repayment_type,guarantee_type,house_property,loan_attention,"
    sql += "(case is_have_loan when 1 then '是' when 0 then '否' end)is_have_loan,"
    sql += "(case is_known_xhnsh when 1 then '知道' when 0 then '不知道' end)is_known_xhnsh,business_with_xhnsh,"
    sql += "(case is_need_service when 1 then '手机银行' when 2 then '转账电话' when 3 then 'pos机' when 4 then '网上银行' when 5 then '借记卡' when 6 then '贷记卡' when 7 then '无需求' end)is_need_service "
    #sql += "status "
    sql += "FROM (select * from sc_target_customer where "
    sql += " 1=1"
    if manager != '0':
        sql += " and receiver="+manager
    sql += " and create_date between '"+beg_date+"' and '"+end_date + "' "
    if customer_name:
        sql += " and (customer_name like '%"+customer_name+"%' or shop_name like '%"+customer_name+"%') "
    sql += ")sc_target_customer INNER JOIN sc_user ON sc_target_customer.receiver = sc_user.id "
    sql += "left JOIN sc_industry ON sc_target_customer.industry = sc_industry.id "
    sql += "left JOIN sc_loan_purpose ON sc_target_customer.loan_purpose = sc_loan_purpose.id "
    sql += "left JOIN sc_business_type ON sc_target_customer.business_type = sc_business_type.id "

    data=db.engine.execute(sql)
    #for row in data:
    #    row['reception_type'] = my_dic['reception_type'][str(dic['reception_type'])]

    exl_hdngs=['营销人','营销方式','营销时间','营销状态','客户状态','是否向小微支行填写申请表？',#1
        '备注','客户名称','电话','性别','年龄','地址','所属行业','经营内容',#2
        '店铺名称','经营期限','资产规模','月销售额','雇员数量','企业类别',#3
        '是否有贷款需求','贷款目的','贷款数额','希望的还款方式','能提供的担保方式','房产产权情况','贷款关注程度',#4
        '是否在他行有借款','知道兴化农商行吗？','您在兴化农村商业银行办理过什么业务？','您是否需要办理以下银行产品']#5

    type_str = 'text text date text text text text text'#1
    type_str += ' text text text text text text text text'#2
    type_str += ' text text text text text text'#3
    type_str += ' text text text text text text text'#4
    type_str += ' text text text text'#5

    types= type_str.split()

    exl_hdngs_xf=ezxf('font: bold on;align: wrap on,vert centre,horiz center')
    types_to_xf_map={
        'int':ezxf(num_format_str='#,##0'),
        'date':ezxf(num_format_str='yyyy-mm-dd'),
        'datetime':ezxf(num_format_str='yyyy-mm-dd HH:MM:SS'),
        'ratio':ezxf(num_format_str='#,##0.00%'),
        'text':ezxf(),
        'price':ezxf(num_format_str='￥#,##0.00')
    }

    data_xfs=[types_to_xf_map[t] for t in types]
    date=datetime.datetime.now()
    year=date.year
    month=date.month
    day=date.day
    filename=str(year)+'_'+str(month)+'_'+str(day)+'_'+'来访登记统计表'+'.xls'
    exp=export_excel()
    return exp.export_download(filename,'来访登记统计表',exl_hdngs,data,exl_hdngs_xf,data_xfs)

# 新增来访登记
@app.route('/Information/lfdj/new_lfdj', methods=['GET','POST'])
def new_lfdj():
    if request.method == 'POST' :
        try:
            reception_type = request.form['reception_type']

            yingxiao_status = request.form['yingxiao_status']
            client_status = request.form['client_status']
            is_apply_form = request.form['is_apply_form']
            remark = request.form['remark']

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
                yingxiao_status,client_status,is_apply_form,
                customer_name,mobile,sex,age,address,
                industry,business_content,shop_name,period,property_scope,monthly_sales,employees,
                business_type,is_need_loan,loan_purpose,loan_amount,repayment_type,guarantee_type,
                house_property,loan_attention,is_have_loan,is_known_xhnsh,business_with_xhnsh,
                is_need_service,0,None,None,None,0,remark).add()

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
            target_customer.remark = request.form['remark']
            
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