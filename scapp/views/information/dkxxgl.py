# coding:utf-8
from flask import Module, session, request, render_template, redirect, url_for

from scapp.models import SC_Loan_Apply
from scapp.models import SC_Apply_Info
from scapp.models import SC_Approval_Decision
from scapp.models import SC_Loan_Purpose
from scapp.models import SC_Individual_Customer
from scapp.models import SC_Company_Customer
from scapp.models import SC_Manage_Info
from scapp.models import SC_User
from scapp.models import SC_Financial_Affairs
from scapp.models import SC_Loan_Purpose
from scapp.models import SC_Credit_History
from scapp.models import SC_Co_Borrower
from scapp.models import SC_Guarantees_For_Others
from scapp.models import SC_Guaranty
from scapp.models import SC_Guarantees
from scapp.models import SC_Riskanalysis_And_Findings
from scapp.models.credit_data.sc_cross_examination import SC_Cross_Examination
from scapp.models.credit_data.sc_balance_sheet import SC_Balance_Sheet
from scapp.models.credit_data.sc_profit_loss import SC_Profit_Loss
from scapp.models.repayment.sc_repayment_plan import SC_Repayment_Plan
from scapp.models.repayment.sc_repayment_plan_detail import SC_Repayment_plan_detail
from scapp.models.credit_data.sc_cash_flow import SC_Cash_Flow
from scapp.models.credit_data.sc_cash_flow_assist import SC_Cash_Flow_Assist
from scapp.models.credit_data.sc_cash_flow_dec import SC_Cash_Flow_Dec
from scapp.models.credit_data.sc_dydb_dec import SC_Dydb_Dec
from scapp.models.credit_data.sc_fixed_assets_car import SC_Fixed_Assets_Car
from scapp.models.credit_data.sc_fixed_assets_estate import SC_Fixed_Assets_Estate
from scapp.models.credit_data.sc_fixed_assets_equipment import SC_Fixed_Assets_Equipment
from scapp.models.credit_data.sc_stock import SC_Stock
from scapp.models.credit_data.sc_accounts_list import SC_Accounts_List
from scapp.config import PER_PAGE
from scapp.models import View_Query_Loan

from scapp.models import SC_Loan_Product

from scapp import app

# 贷款信息管理
@app.route('/Information/dkxxgl', methods=['GET'])
def dkxxgl():
    loan_product = SC_Loan_Product.query.all()
    return render_template("Information/dkxxgl_search.html",loan_product=loan_product)

# 贷款信息管理
@app.route('/Information/dkxxgl_search/<int:page>', methods=['POST'])
def dkxxgl_search(page):
    customer_name = request.form['customer_name']
    loan_type = request.form['loan_type']
    sql = " 1=1"
    if loan_type != '0':
        sql = " and loan_type='"+loan_type+"'"

    if customer_name:
        sql += " and (company_customer_name like '%"+customer_name+"%' or individual_customer_name like '%"+customer_name+"%')"

    loan_apply = View_Query_Loan.query.filter(sql).paginate(page, per_page = PER_PAGE)
    loan_product = SC_Loan_Product.query.all()
    return render_template("Information/dkxxgl.html",loan_apply=loan_apply,customer_name=customer_name,loan_type=loan_type,loan_product=loan_product)
	
# 贷款信息管理——贷款信息
@app.route('/Information/dkxx/<int:loan_apply_id>', methods=['GET'])
def dkxx(loan_apply_id):
    loan_apply = SC_Loan_Apply.query.filter_by(id=loan_apply_id).first()
    return render_template("Information/dkxx.html",loan_apply=loan_apply)

# 贷款信息管理用——贷款信息--基础信息
@app.route('/Information/dkxx/jcxx/<int:loan_apply_id>', methods=['GET'])
def dkxx_jcxx(loan_apply_id):
    loan_apply = SC_Loan_Apply.query.filter_by(id=loan_apply_id).first()
    apply_info = SC_Apply_Info.query.filter_by(loan_apply_id=loan_apply_id).first()
    loan_purpose = SC_Loan_Purpose.query.order_by("id").all()
    approval_decision = SC_Approval_Decision.query.filter_by(loan_apply_id=loan_apply_id).first()
    
    loan_product = SC_Loan_Product.query.all()
    
    return render_template("Information/dkxx/jcxx.html",loan_apply=loan_apply,apply_info=apply_info,loan_purpose=loan_purpose,
        approval_decision=approval_decision,loan_product=loan_product)

# 贷款信息管理用——贷款信息--还款计划
@app.route('/Information/dkxx/hkjh/<int:loan_apply_id>', methods=['GET'])
def dkxx_hkjh(loan_apply_id):
    loan_apply = SC_Loan_Apply.query.filter_by(id=loan_apply_id).first()
    approval_decision = SC_Approval_Decision.query.filter_by(loan_apply_id=loan_apply_id).first()
    repayment_plan_detail = SC_Repayment_plan_detail.query.filter_by(loan_apply_id=loan_apply_id,change_record=1).order_by("id").all()
    return render_template("Information/dkxx/hkjh.html",loan_apply=loan_apply,approval_decision=approval_decision,
        repayment_plan_detail=repayment_plan_detail)

# 贷款信息管理用——审批信息--申请表
@app.route('/Information/dkxx/dksqsh_info/<belong_customer_type>/<int:belong_customer_value>/<int:id>', methods=['GET'])
def dkxx_dksqsh_info(belong_customer_type,belong_customer_value,id):
    
    if belong_customer_type == 'Company':
        customer = SC_Company_Customer.query.filter_by(id=belong_customer_value).first()
    else :
        customer = SC_Individual_Customer.query.filter_by(id=belong_customer_value).first()

    loan_apply = SC_Loan_Apply.query.filter_by(id=id).first()
    manager_info = SC_Manage_Info.query.filter_by(belong_customer_type=belong_customer_type,
        belong_customer_value=belong_customer_value).first()
    financial_affairs = SC_Financial_Affairs.query.filter_by(belong_customer_type=belong_customer_type,
        belong_customer_value=belong_customer_value).first()
    user = SC_User.query.order_by("id").all()
    loan_purpose = SC_Loan_Purpose.query.order_by("id").all()
    apply_info = SC_Apply_Info.query.filter_by(loan_apply_id=id).first()
    credit_history = SC_Credit_History.query.filter_by(loan_apply_id=id).all()
    co_borrower = SC_Co_Borrower.query.filter_by(loan_apply_id=id).all()
    guarantees_for_others = SC_Guarantees_For_Others.query.filter_by(loan_apply_id=id).all()
    guaranty = SC_Guaranty.query.filter_by(loan_apply_id=id).all()
    guarantees = SC_Guarantees.query.filter_by(loan_apply_id=id).all()
    
    loan_product = SC_Loan_Product.query.all()
    
    return render_template("Information/dkxx/dksqsh_info.html",belong_customer_type=belong_customer_type,belong_customer_value=belong_customer_value,
        customer=customer,loan_apply=loan_apply,manager_info=manager_info,financial_affairs=financial_affairs,user=user,
        loan_purpose=loan_purpose,apply_info=apply_info,credit_history=credit_history
        ,co_borrower=co_borrower,guarantees_for_others=guarantees_for_others,guaranty=guaranty
        ,guarantees=guarantees,loan_product=loan_product)

# 贷款信息管理用——审批信息--调查表--微贷款(基本情况)
@app.route('/Information/dkxx/dqdcWd_jbqk/<belong_customer_type>/<int:belong_customer_value>/<int:id>', methods=['GET'])
def dkxx_dqdcWd_jbqk(belong_customer_type,belong_customer_value,id):
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

    return render_template("Information/dkxx/dqdcWd_jbqk.html",belong_customer_type=belong_customer_type,
        belong_customer_value=belong_customer_value,id=id,customer=customer,loan_apply=loan_apply,
        apply_info=apply_info,loan_purpose=loan_purpose,credit_history=credit_history,
        co_borrower=co_borrower,guaranty=guaranty,guarantees=guarantees,
        riskanalysis_and_findings=riskanalysis_and_findings)

# 贷款信息管理用——审批信息--调查表--微贷款(资产负债表)
@app.route('/Information/dkxx/dqdcWd_zcfzb/<int:loan_apply_id>', methods=['GET'])
def dkxx_dqdcWd_zcfzb(loan_apply_id):
    balance_sheets = SC_Balance_Sheet.query.filter_by(loan_apply_id=loan_apply_id).order_by("id").all()
    count_0 = SC_Balance_Sheet.query.filter_by(loan_apply_id=loan_apply_id,loan_type=0).count()
    count_2 = SC_Balance_Sheet.query.filter_by(loan_apply_id=loan_apply_id,loan_type=2).count()
    count_4 = SC_Balance_Sheet.query.filter_by(loan_apply_id=loan_apply_id,loan_type=4).count()
    count_6 = SC_Balance_Sheet.query.filter_by(loan_apply_id=loan_apply_id,loan_type=6).count()
    count_10 = SC_Balance_Sheet.query.filter_by(loan_apply_id=loan_apply_id,loan_type=10).count()
    count_12 = SC_Balance_Sheet.query.filter_by(loan_apply_id=loan_apply_id,loan_type=12).count()
    return render_template("Information/dkxx/dqdcWd_zcfzb.html",loan_apply_id=loan_apply_id,
        balance_sheets=balance_sheets,count_0=count_0,count_2=count_2,count_4=count_4,count_6=count_6,
        count_10=count_10,count_12=count_12)

# 贷款信息管理用——审批信息--调查表--微贷款(损益情况分析)
@app.route('/Information/dkxx/dqdcWd_syb/<int:loan_apply_id>', methods=['GET'])
def dkxx_dqdcWd_syb(loan_apply_id):
    profit_loss = SC_Profit_Loss.query.filter_by(loan_apply_id=loan_apply_id).order_by("id").all()
    count_1 = SC_Profit_Loss.query.filter_by(loan_apply_id=loan_apply_id,items_type=1).count()
    count_3 = SC_Profit_Loss.query.filter_by(loan_apply_id=loan_apply_id,items_type=3).count()
    count_21 = SC_Profit_Loss.query.filter_by(loan_apply_id=loan_apply_id,items_type=21).count()
    count_28 = SC_Profit_Loss.query.filter_by(loan_apply_id=loan_apply_id,items_type=28).count()
    count_29 = SC_Profit_Loss.query.filter_by(loan_apply_id=loan_apply_id,items_type=29).count()
    return render_template("Information/dkxx/dqdcWd_syb.html",loan_apply_id=loan_apply_id,profit_loss=profit_loss,
        count_1=count_1,count_3=count_3,count_21=count_21,count_28=count_28,count_29=count_29)

# 贷款信息管理用——审批信息--调查表--小额贷款(基本情况)
@app.route('/Information/dkxx/dqdcXed_jbqk/<belong_customer_type>/<int:belong_customer_value>/<int:id>', methods=['GET'])
def dkxx_dqdcXed_jbqk(belong_customer_type,belong_customer_value,id):
    if belong_customer_type == 'Company':
        customer = SC_Company_Customer.query.filter_by(id=belong_customer_value).first()
    else :
        customer = SC_Individual_Customer.query.filter_by(id=belong_customer_value).first()

    loan_apply = SC_Loan_Apply.query.filter_by(id=id).first()
    apply_info = SC_Apply_Info.query.filter_by(loan_apply_id=id).first()
    loan_purpose = SC_Loan_Purpose.query.order_by("id").all()
    credit_history = SC_Credit_History.query.filter_by(loan_apply_id=id).all()
    guarantees_for_others = SC_Guarantees_For_Others.query.filter_by(loan_apply_id=id).all()
    #financial_overview = SC_Financial_Overview.query.filter_by(loan_apply_id=id).first()
    #non_financial_analysis = SC_Non_Financial_Analysis.query.filter_by(loan_apply_id=id).first()
    riskanalysis_and_findings = SC_Riskanalysis_And_Findings.query.filter_by(loan_apply_id=id).first()
    
    return render_template("Information/dkxx/dqdcXed_jbqk.html",belong_customer_type=belong_customer_type,
        belong_customer_value=belong_customer_value,id=id,customer=customer,loan_apply=loan_apply,
        apply_info=apply_info,loan_purpose=loan_purpose,credit_history=credit_history,
        guarantees_for_others=guarantees_for_others,riskanalysis_and_findings=riskanalysis_and_findings)

# 贷款信息管理用——审批信息--调查表--微贷(资产负债表)
@app.route('/Information/dkxx/dqdcXed_zcfzb/<int:loan_apply_id>', methods=['GET'])
def dkxx_dqdcXed_zcfzb(loan_apply_id):
    balance_sheets = SC_Balance_Sheet.query.filter_by(loan_apply_id=loan_apply_id).order_by("id").all()
    count_0 = SC_Balance_Sheet.query.filter_by(loan_apply_id=loan_apply_id,loan_type=0).count()
    count_2 = SC_Balance_Sheet.query.filter_by(loan_apply_id=loan_apply_id,loan_type=2).count()
    count_4 = SC_Balance_Sheet.query.filter_by(loan_apply_id=loan_apply_id,loan_type=4).count()
    count_6 = SC_Balance_Sheet.query.filter_by(loan_apply_id=loan_apply_id,loan_type=6).count()
    count_10 = SC_Balance_Sheet.query.filter_by(loan_apply_id=loan_apply_id,loan_type=10).count()
    count_12 = SC_Balance_Sheet.query.filter_by(loan_apply_id=loan_apply_id,loan_type=12).count()
    return render_template("Information/dkxx/dqdcXed_zcfzb.html",loan_apply_id=loan_apply_id,
        balance_sheets=balance_sheets,count_0=count_0,count_2=count_2,count_4=count_4,count_6=count_6,
        count_10=count_10,count_12=count_12)

# 贷款信息管理用——审批信息--调查表--小额贷款(交叉检验)
@app.route('/Information/dkxx/dqdcXed_jcjy/<int:loan_apply_id>', methods=['GET'])
def dkxx_dqdcXed_jcjy(loan_apply_id):
    cross_examination = SC_Cross_Examination.query.filter_by(loan_apply_id=loan_apply_id).order_by("id").all()
    count_3 = SC_Cross_Examination.query.filter_by(loan_apply_id=loan_apply_id,loan_type=3).count()
    balance_sheet = SC_Balance_Sheet.query.filter_by(loan_apply_id=loan_apply_id,loan_type=16).first()#type=16为资产负债表中的所有者权益
    return render_template("Information/dkxx/dqdcXed_jcjy.html",loan_apply_id=loan_apply_id,
        cross_examination=cross_examination,count_3=count_3,balance_sheet=balance_sheet)

# 贷款信息管理用——审批信息--调查表--小额贷款(损益情况分析)
@app.route('/Information/dkxx/dqdcXed_ysqkfx/<int:loan_apply_id>', methods=['GET'])
def dkxx_dqdcXed_ysqkfx(loan_apply_id):
    profit_loss = SC_Profit_Loss.query.filter_by(loan_apply_id=loan_apply_id).order_by("id").all()
    count_1 = SC_Profit_Loss.query.filter_by(loan_apply_id=loan_apply_id,items_type=1).count()
    count_3 = SC_Profit_Loss.query.filter_by(loan_apply_id=loan_apply_id,items_type=3).count()
    count_21 = SC_Profit_Loss.query.filter_by(loan_apply_id=loan_apply_id,items_type=21).count()
    count_28 = SC_Profit_Loss.query.filter_by(loan_apply_id=loan_apply_id,items_type=28).count()
    count_29 = SC_Profit_Loss.query.filter_by(loan_apply_id=loan_apply_id,items_type=29).count()
    return render_template("Information/dkxx/dqdcXed_ysqkfx.html",loan_apply_id=loan_apply_id,profit_loss=profit_loss,
        count_1=count_1,count_3=count_3,count_21=count_21,count_28=count_28,count_29=count_29)

# 贷款信息管理用——审批信息--调查表--小额贷款(现金流分析)
@app.route('/Information/dkxx/dqdcXed_xjlfx/<int:id>', methods=['GET'])
def dkxx_dqdcXed_xjlfx(id):
    cash_flow = SC_Cash_Flow.query.filter_by(loan_apply_id=id,type=1).all()
    cash_flow_assist_0 = SC_Cash_Flow_Assist.query.filter_by(loan_apply_id=id,type=1,assist_type=0).all()
    cash_flow_assist_1 = SC_Cash_Flow_Assist.query.filter_by(loan_apply_id=id,type=1,assist_type=1).all()
    cash_flow_assist_2 = SC_Cash_Flow_Assist.query.filter_by(loan_apply_id=id,type=1,assist_type=2).all()
    cash_flow_assist_3 = SC_Cash_Flow_Assist.query.filter_by(loan_apply_id=id,type=1,assist_type=3).all()
    if len(cash_flow) == 0: #用空串初始化cash_flow
        cash_flow = [0 for i in range(13)]
        cash_flow = ['']*13

    cash_flow_dec = SC_Cash_Flow_Dec.query.filter_by(loan_apply_id=id).first()

    return render_template("Information/dkxx/dqdcXed_xjlfx.html",id=id,cash_flow=cash_flow,
        cash_flow_assist_0=cash_flow_assist_0,cash_flow_assist_1=cash_flow_assist_1,
        cash_flow_assist_2=cash_flow_assist_2,cash_flow_assist_3=cash_flow_assist_3,
        cash_flow_dec=cash_flow_dec)

# 贷款信息管理用——审批信息--调查表--小额贷款(担保抵押调查表)
@app.route('/Information/dkxx/dqdcXed_dbdydcb/<int:id>', methods=['GET'])
def dkxx_dqdcXed_dbdydcb(id):
    co_borrower = SC_Co_Borrower.query.filter_by(loan_apply_id=id).all()
    guaranty = SC_Guaranty.query.filter_by(loan_apply_id=id).all()
    guarantees = SC_Guarantees.query.filter_by(loan_apply_id=id).all()

    dydb_dec = SC_Dydb_Dec.query.filter_by(loan_apply_id=id).first()

    return render_template("Information/dkxx/dqdcXed_dbdydcb.html",id=id,co_borrower=co_borrower,guaranty=guaranty,
        guarantees=guarantees,dydb_dec=dydb_dec)

# 贷款信息管理用——审批信息--调查表--小额贷款(固定资产清单)
@app.route('/Information/dkxx/dqdcXed_gdzcqd/<int:id>', methods=['GET'])
def dkxx_dqdcXed_gdzcqd(id):
    fixed_assets_estate = SC_Fixed_Assets_Estate.query.filter_by(loan_apply_id=id).all()
    fixed_assets_equipment = SC_Fixed_Assets_Equipment.query.filter_by(loan_apply_id=id).all()
    fixed_assets_car = SC_Fixed_Assets_Car.query.filter_by(loan_apply_id=id).all()

    return render_template("Information/dkxx/dqdcXed_gdzcqd.html",id=id,fixed_assets_estate=fixed_assets_estate,
        fixed_assets_equipment=fixed_assets_equipment,fixed_assets_car=fixed_assets_car)

# 贷款信息管理用——审批信息--调查表--小额贷款(库存)
@app.route('/Information/dkxx/dqdcXed_kc/<int:loan_apply_id>', methods=['GET'])
def dkxx_dqdcXed_kc(loan_apply_id):
    stocks = SC_Stock.query.filter_by(loan_apply_id=loan_apply_id).all()
    return render_template("Information/dkxx/dqdcXed_kc.html",loan_apply_id=loan_apply_id,stocks=stocks)

# 贷款信息管理用——审批信息--调查表--小额贷款(账款清单)
@app.route('/Information/dkxx/dqdcXed_zkqd/<int:id>', methods=['GET'])
def dkxx_dqdcXed_zkqd(id):
    accounts_list = SC_Accounts_List.query.filter_by(loan_apply_id=id).all()
    return render_template("Information/dkxx/dqdcXed_zkqd.html",id=id,accounts_list=accounts_list)

# 贷款信息管理用——审批信息--调查表--审贷会决议单
@app.route('/Information/dkxx/edit_sdhjyd/<int:loan_apply_id>', methods=['GET'])
def dkxx_edit_sdhjyd(loan_apply_id):
    loan_apply = SC_Loan_Apply.query.filter_by(id=loan_apply_id).first()
    riskanalysis_and_findings = SC_Riskanalysis_And_Findings.query.filter_by(loan_apply_id=loan_apply_id).first()
    approval_decision = SC_Approval_Decision.query.filter_by(loan_apply_id=loan_apply_id).first()
    co_borrower = SC_Co_Borrower.query.filter_by(loan_apply_id=loan_apply_id).all()
    guaranty = SC_Guaranty.query.filter_by(loan_apply_id=loan_apply_id).all()
    guaranty = SC_Guaranty.query.filter_by(loan_apply_id=loan_apply_id).all()
    guarantees = SC_Guarantees.query.filter_by(loan_apply_id=loan_apply_id).all()

    if loan_apply.belong_customer_type == 'Company':
        customer = SC_Company_Customer.query.filter_by(id=loan_apply.belong_customer_value).first()
    else :
        customer = SC_Individual_Customer.query.filter_by(id=loan_apply.belong_customer_value).first()

    return render_template("Information/dkxx/edit_sdhjyd.html",loan_apply_id=loan_apply_id,
        riskanalysis_and_findings=riskanalysis_and_findings,customer=customer,
        approval_decision=approval_decision,co_borrower=co_borrower,guaranty=guaranty,
        guarantees=guarantees)

# 贷款放款——编辑放款(放款信息)
@app.route('/Information/dkxx/fkxx/<int:loan_apply_id>', methods=['GET'])
def dkxx_dkfk_fkxx(loan_apply_id):
    approval_decision = SC_Approval_Decision.query.filter_by(loan_apply_id=loan_apply_id).first()
    return render_template("Information/dkxx/fkxx.html",approval_decision=approval_decision)

# 贷款信息管理——贷款信息(还款记录)
@app.route('/Information/dkxx_hkjl', methods=['GET'])
def dkxx_hkjl():
    return render_template("Information/dkxx_hkjl.html")

# 贷款信息管理——贷款信息(还款记录明细)
@app.route('/Information/dkxx_hkjlInfo', methods=['GET'])
def dkxx_hkjlInfo():
    return render_template("Information/dkxx_hkjlInfo.html")

# 贷款信息管理——贷款信息(贷后变更)
@app.route('/Information/dkxx_dhbg', methods=['GET'])
def dkxx_dhbg():
    return render_template("Information/dkxx_dhbg.html")

# 贷款信息管理——贷款信息(贷后变更——修改还款计划)
@app.route('/Information/dkxx_dhbg_xghkjh', methods=['GET'])
def dkxx_dhbg_xghkjh():
    return render_template("Information/dkxx_dhbg_xghkjh.html")

# 贷款信息管理——贷款信息(贷后变更——修改担保人)
@app.route('/Information/dkxx_dhbg_xgdbrsj', methods=['GET'])
def dkxx_dhbg_xgdbrsj():
    return render_template("Information/dkxx_dhbg_xgdbrsj.html")

# 贷款信息管理——贷款信息(贷后变更——修改共同借款人)
@app.route('/Information/dkxx_dhbg_xggtjkr', methods=['GET'])
def dkxx_dhbg_xggtjkr():
    return render_template("Information/dkxx_dhbg_xggtjkr.html")

# 贷款信息管理——贷款信息(贷后变更——修改抵质押信息)
@app.route('/Information/dkxx_dhbg_xgdzyxx', methods=['GET'])
def dkxx_dhbg_xgdzyxx():
    return render_template("Information/dkxx_dhbg_xgdzyxx.html")