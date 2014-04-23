# coding:utf-8

import os

from flask import Module, session, request, render_template, redirect, url_for,flash
from flask.ext.login import current_user
import datetime,time,xlwt
ezxf=xlwt.easyxf #样式转换

from scapp import db
from scapp.config import logger
from scapp.config import PER_PAGE
from scapp.config import PROCESS_STATUS_DKSQ

from scapp.tools.export_excel import export_excel

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
from scapp.models import SC_Risk_Level

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
    customer_name = request.form['customer_name']
    loan_type = request.form['loan_type']
    sql = ""
    if loan_type != '0':
        sql = "loan_type='"+loan_type+"' and "
    sql += " marketing_loan_officer="+str(current_user.id)+" and process_status='"+PROCESS_STATUS_DKSQ+"'"

    if customer_name:
        sql += " and (company_customer_name like '%"+customer_name+"%' or individual_customer_name like '%"+customer_name+"%')"

    loan_apply = View_Query_Loan.query.filter(sql).paginate(page, per_page = PER_PAGE)
    return render_template("Process/dksq/dksq.html",loan_apply=loan_apply,customer_name=customer_name,loan_type=loan_type)

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
    risk_level = SC_Risk_Level.query.order_by("id").all()

    return render_template("Process/dksq/new_dksq_info.html",belong_customer_type=belong_customer_type,
        customer=customer,manager_info=manager_info,financial_affairs=financial_affairs,
        loan_purpose=loan_purpose,risk_level=risk_level)

# 新增贷款申请信息
@app.route('/Process/dksq/new_dksq/<belong_customer_type>/<int:belong_customer_value>', methods=['POST'])
def new_dksq(belong_customer_type,belong_customer_value):
    try:
        #生成贷款申请表
        loan_apply = SC_Loan_Apply(request.form['loan_type'],belong_customer_type,belong_customer_value,request.form['customer_name'],request.form['evaluation'],
            current_user.id,None,None,None,None,None,None,PROCESS_STATUS_DKSQ,request.form['risk_level'])
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
        home_addr_list = request.form.getlist('home_addr')
        hj_addr_list = request.form.getlist('hj_addr')
        home_list = request.form.getlist('home')
        remark_list = request.form.getlist('remark')
        # 循环获取表单
        for i in range(len(name_list)):
            SC_Co_Borrower(loan_apply.id,name_list[i],relationship_list[i],
                id_number_list[i],phone_list[i],main_business_list[i],
                address_list[i],major_assets_list[i],monthly_income_list[i],
                home_addr_list[i],
                hj_addr_list[i],
                home_list[i],
                remark_list[i]).add()

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
    risk_level = SC_Risk_Level.query.order_by("id").all()
    apply_info = SC_Apply_Info.query.filter_by(loan_apply_id=id).first()
    credit_history = SC_Credit_History.query.filter_by(loan_apply_id=id).all()
    co_borrower = SC_Co_Borrower.query.filter_by(loan_apply_id=id).all()
    guarantees_for_others = SC_Guarantees_For_Others.query.filter_by(loan_apply_id=id).all()
    guaranty = SC_Guaranty.query.filter_by(loan_apply_id=id).all()
    guarantees = SC_Guarantees.query.filter_by(loan_apply_id=id).all()

    return render_template("Process/dksq/edit_dksq_info.html",belong_customer_type=belong_customer_type,belong_customer_value=belong_customer_value,
        customer=customer,loan_apply=loan_apply,manager_info=manager_info,financial_affairs=financial_affairs,
        loan_purpose=loan_purpose,risk_level=risk_level,apply_info=apply_info,credit_history=credit_history
        ,co_borrower=co_borrower,guarantees_for_others=guarantees_for_others,guaranty=guaranty
        ,guarantees=guarantees)

# 编辑贷款申请信息
@app.route('/Process/dksq/edit_dksq/<int:id>', methods=['POST'])
def edit_dksq(id):

    try:
        #保存贷款申请表
        SC_Loan_Apply.query.filter_by(id=id).update({"loan_type":request.form['loan_type'],
            "evaluation":request.form['evaluation'],"marketing_loan_officer":current_user.id,
            "modify_user":current_user.id,"modify_date":datetime.datetime.now(),"risk_level":request.form['risk_level']})

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
        home_addr_list = request.form.getlist('home_addr')
        hj_addr_list = request.form.getlist('hj_addr')
        home_list = request.form.getlist('home')
        remark_list = request.form.getlist('remark')
        # 循环获取表单
        for i in range(len(name_list)):
            SC_Co_Borrower(loan_apply.id,name_list[i],relationship_list[i],
                id_number_list[i],phone_list[i],main_business_list[i],
                address_list[i],major_assets_list[i],monthly_income_list[i],
                home_addr_list[i],hj_addr_list[i],home_list[i],remark_list[i]).add()
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

# 导出已填写申请的客户信息
@app.route('/Process/dksq/goto_export_customer_info/<belong_customer_type>', methods=['GET'])
def goto_export_customer_info(belong_customer_type):
    if belong_customer_type == 'Company':
        print 'do nothing'
    else :
        sql = "select 'Ind01' as zjlx,credentials_no,'321281055' as ghjg,customer_name,'L025503' as ghrbh,"#1
        sql += "'356' as hjbh,if(sex='1','1','2') as xb,birthday,residence_address,'1' as sfhz,"#2
        sql += "'71' as jtjs,'2' as sfgd,'2' as sfsy,'2' as sfgxr,'01' as mz,"#3
        sql += "'04' as zzmm,if(marriage='0','10','20') as hyzk,'001' as jkzk,'10' as zgxl,'1' as zgxw,'' as gzdw,"#4
        sql += "'1' as zw,'1' as zc,'' as dzm,'1' as sfxyh,residence,"#5
        sql += "'1' as sfxyx,residence_address as xzcmc,'1' as sfxyc,living_conditions,home_address,"#6
        sql += "zip_code,telephone,mobile,'' as email,profession,"#7
        sql += "'2' as sfzhsx,'' as zhsxyy,'' as ydtkh,'' as jszh,'' as tdmj,"#8
        sql += "create_date,'' as wycs,'' as ckye,'' as yyck,'010' as jjms,"#9
        sql += "'' as jygm,'' as jydz,'' as jyxm, '' as xqm,'' as fczh,"#10
        sql += "'' as fwmj,'' as jqxydj,'' as jqpjsj,'' as bz"#11
        sql += " from sc_individual_customer where is_have_export = '0'"

        data=db.engine.execute(sql)

        exl_hdngs = ['证件类型(*)','证件号码(*)','管户机构(*)','姓名(*)','管户人编号(*)', #1
            '户籍编号（*）','性别（*）','出生日期（*）','户籍地址','是否为户主（*）',#2
            '家庭角色','是否本行/社股东','是否本行/社员工','是否本行/社其他关系人','民族',#3
            '政治面貌','婚姻状况','健康状况','最高学历','最高学位','工作单位名称',#4
            '职务','职称','地址码','是否信用户','所属行政乡(镇)',#5
            '是否信用乡（镇）','所属行政村名称','是否信用村','居住状况','居住地址',#6
            '居住地址邮编','住宅电话','联系号码（短信提醒）','电子邮箱','职业（国标）',#7
            '是否暂缓授信','暂缓授信原因','易贷通卡号','本行/社结算账户','承包土地面积',#8
            '与我行首次建立信贷关系时间','违约次数','一年日均存款金额','预约存款','经营模式',#9
            '经营规模','经营地址','主要经营项目及收入来源','房屋小区名','房产证号',#10
            '房屋面积','即期信用等级','即期评级时间','备注']#11

        type_str = 'text text text text text'#1
        type_str += ' text text date text text'#2
        type_str += ' text text text text text'#3
        type_str += ' text text text text text text'#4
        type_str += ' text text text text text'#5
        type_str += ' text text text text text'#6
        type_str += ' text text text text text'#7
        type_str += ' text text text text text'#8
        type_str += ' date text text text text'#9
        type_str += ' text text text text text'#10
        type_str += ' text text date text'#11

        types = type_str.split()
        exl_hdngs_xf=ezxf('font: bold on;align: wrap on,vert centre,horiz center')
        types_to_xf_map={
            'int':ezxf(num_format_str='#,##0'),
            'date':ezxf(num_format_str='yyyy/mm/dd'),
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
        filename=str(year)+'_'+str(month)+'_'+str(day)+'_'+'客户信息表'+'.xls'
        exp=export_excel()
        return exp.export_download(filename,'客户信息表',exl_hdngs,data,exl_hdngs_xf,data_xfs)