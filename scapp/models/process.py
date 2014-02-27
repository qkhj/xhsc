#coding:utf-8
from flask.ext.login import current_user

from scapp import db
import datetime

# 贷款申请
class SC_Loan_Apply(db.Model):
    __tablename__ = 'sc_loan_apply' 
    id = db.Column(db.Integer, primary_key=True)
    loan_type = db.Column(db.Integer) #贷款类型 微贷:1 小额贷:2
    belong_customer_type = db.Column(db.String(32)) #客户类型 Company 或者 Individual
    belong_customer_value = db.Column(db.Integer) #客户id
    customer_name = db.Column(db.String(128)) #处理状态
    evaluation = db.Column(db.String(256)) #评价
    marketing_loan_officer = db.Column(db.Integer, db.ForeignKey('sc_user.id')) #营销信贷员
    A_loan_officer = db.Column(db.Integer, db.ForeignKey('sc_user.id')) #A岗信贷员
    B_loan_officer = db.Column(db.Integer, db.ForeignKey('sc_user.id')) #B岗信贷员
    yunying_loan_officer = db.Column(db.Integer, db.ForeignKey('sc_user.id')) #运营岗信贷员
    examiner_1 = db.Column(db.Integer, db.ForeignKey('sc_user.id')) #审查人
    examiner_2 = db.Column(db.Integer, db.ForeignKey('sc_user.id')) #审查人
    approver = db.Column(db.Integer, db.ForeignKey('sc_user.id')) #审批人
    process_status = db.Column(db.String(4)) #处理状态
    classify = db.Column(db.Integer) #资产分类
    classify_dec = db.Column(db.String(256)) #资产分类说明
    create_user = db.Column(db.Integer)
    create_date = db.Column(db.DateTime)
    modify_user = db.Column(db.Integer)
    modify_date = db.Column(db.DateTime)
   
    # 外键名称
    marketing_loan_officer_name = db.relationship('SC_User',foreign_keys=[marketing_loan_officer],backref = db.backref('marketing_loan_officer_name', lazy = 'dynamic'))
    # 外键名称
    A_loan_officer_name = db.relationship('SC_User',foreign_keys=[A_loan_officer], backref = db.backref('A_loan_officer_name', lazy = 'dynamic'))
    # 外键名称
    B_loan_officer_name = db.relationship('SC_User',foreign_keys=[B_loan_officer], backref = db.backref('B_loan_officer_name', lazy = 'dynamic'))
    # 外键名称
    yunying_loan_officer_name = db.relationship('SC_User',foreign_keys=[yunying_loan_officer], backref = db.backref('yunying_loan_officer_name', lazy = 'dynamic'))
    # 外键名称
    examiner_1_name = db.relationship('SC_User',foreign_keys=[examiner_1], backref = db.backref('examiner_1_name', lazy = 'dynamic'))
    # 外键名称
    examiner_2_name = db.relationship('SC_User',foreign_keys=[examiner_2], backref = db.backref('examiner_2_name', lazy = 'dynamic'))
    # 外键名称
    approver_name = db.relationship('SC_User',foreign_keys=[approver], backref = db.backref('approver_name', lazy = 'dynamic'))


    def __init__(self,loan_type,belong_customer_type,belong_customer_value,customer_name,
        evaluation,marketing_loan_officer,A_loan_officer,B_loan_officer,
        yunying_loan_officer,examiner_1,examiner_2,approver,process_status):
        self.loan_type = loan_type
        self.belong_customer_type = belong_customer_type
        self.belong_customer_value = belong_customer_value
        self.customer_name = customer_name
        self.evaluation = evaluation
        self.marketing_loan_officer = marketing_loan_officer
        self.A_loan_officer = A_loan_officer
        self.B_loan_officer = B_loan_officer
        self.yunying_loan_officer = yunying_loan_officer
        self.examiner_1 = examiner_1
        self.examiner_2 = examiner_2
        self.approver = approver
        self.process_status = process_status
        self.classify = 1
        self.classify_dec = ''
        self.create_user = current_user.id
        self.create_date = datetime.datetime.now()
        self.modify_user = current_user.id
        self.modify_date = datetime.datetime.now()

    def add(self):
        db.session.add(self)

# 申请信息
class SC_Apply_Info(db.Model):
    __tablename__ = 'sc_apply_info' 
    id = db.Column(db.Integer, primary_key=True)
    loan_apply_id=db.Column(db.Integer)
    loan_amount_num = db.Column(db.String(16)) #贷款金额（元）
    loan_deadline = db.Column(db.String(16)) #贷款期限（月）
    month_repayment = db.Column(db.String(16)) #月还款能力（元）
    loan_purpose = db.Column(db.Integer, db.ForeignKey('sc_loan_purpose.id')) #贷款用途
    details = db.Column(db.String(256))#详细说明
    repayment_source = db.Column(db.String(256)) #还款来源
    #repayment_type = db.Column(db.Integer) #还款方式
    #annual_interest_rate = db.Column(db.String(16)) #月利率
    
    # 外键名称
    loan_purpose_name = db.relationship('SC_Loan_Purpose', backref = db.backref('loan_purpose_name', lazy = 'dynamic'))

    def __init__(self,loan_apply_id,loan_amount_num,loan_deadline,
                month_repayment,loan_purpose,details,repayment_source):
        self.loan_apply_id = loan_apply_id
        self.loan_amount_num = loan_amount_num
        self.loan_deadline = loan_deadline
        self.month_repayment = month_repayment
        self.loan_purpose = loan_purpose
        self.details = details
        self.repayment_source = repayment_source

    def add(self):
        db.session.add(self)

# 信贷历史
class SC_Credit_History(db.Model):
    __tablename__ = 'sc_credit_history' 
    id = db.Column(db.Integer, primary_key=True)
    loan_apply_id=db.Column(db.Integer)
    financing_sources = db.Column(db.String(256)) #融资来源
    loan_amount = db.Column(db.String(16)) #贷款金额(元)
    deadline = db.Column(db.String(16)) #期限
    use = db.Column(db.String(256)) #用途
    release_date = db.Column(db.Date)#发放日期
    overage = db.Column(db.String(16)) #余额(元)
    guarantee = db.Column(db.String(32)) #担保
    late_information = db.Column(db.String(256)) #逾期信息

    def __init__(self,loan_apply_id,financing_sources,loan_amount,
                deadline,use,release_date,overage,guarantee,late_information):
        self.loan_apply_id = loan_apply_id
        self.financing_sources = financing_sources
        self.loan_amount = loan_amount
        self.deadline = deadline
        self.use = use
        self.release_date = release_date
        self.overage = overage
        self.guarantee = guarantee
        self.late_information = late_information

    def add(self):
        db.session.add(self)

# 共同借款人
class SC_Co_Borrower(db.Model):
    __tablename__ = 'sc_co_borrower' 
    id = db.Column(db.Integer, primary_key=True)
    loan_apply_id=db.Column(db.Integer)
    name = db.Column(db.String(32)) #姓名
    relationship = db.Column(db.String(32)) #与客户关系
    id_number = db.Column(db.String(32)) #身份证号码
    phone = db.Column(db.String(32)) #家庭电话
    main_business = db.Column(db.String(128))#主营业务或职务（如受雇与别人）
    address = db.Column(db.String(256)) #经营地址或工作单位地址
    major_assets = db.Column(db.String(256)) #主要资产
    monthly_income = db.Column(db.String(16)) #月收入

    def __init__(self,loan_apply_id,name,relationship,
                id_number,phone,main_business,address,major_assets,monthly_income):
        self.loan_apply_id = loan_apply_id
        self.name = name
        self.relationship = relationship
        self.id_number = id_number
        self.phone = phone
        self.main_business = main_business
        self.address = address
        self.major_assets = major_assets
        self.monthly_income = monthly_income

    def add(self):
        db.session.add(self)

# 是否为他人担保
class SC_Guarantees_For_Others(db.Model):
    __tablename__ = 'sc_guarantees_for_others' 
    id = db.Column(db.Integer, primary_key=True)
    loan_apply_id=db.Column(db.Integer)
    bank = db.Column(db.String(32)) #银行
    guarantor = db.Column(db.String(32)) #被担保人
    guarantee_amount = db.Column(db.String(16)) #担保金额

    def __init__(self,loan_apply_id,bank,guarantor,guarantee_amount):
        self.loan_apply_id = loan_apply_id
        self.bank = bank
        self.guarantor = guarantor
        self.guarantee_amount = guarantee_amount

    def add(self):
        db.session.add(self)

# 有无抵押物
class SC_Guaranty(db.Model):
    __tablename__ = 'sc_guaranty' 
    id = db.Column(db.Integer, primary_key=True)
    loan_apply_id=db.Column(db.Integer)
    obj_name = db.Column(db.String(32)) #物品名称
    owner_address = db.Column(db.String(128)) #所有者、地址
    description = db.Column(db.String(256)) #描述
    registration_number = db.Column(db.String(32)) #登记号
    appraisal = db.Column(db.String(16)) #估价(元)
    mortgage = db.Column(db.String(16)) #抵押(元)
    bool_mortgage = db.Column(db.Integer) #是否抵押

    def __init__(self,loan_apply_id,obj_name,owner_address,description,
        registration_number,appraisal,mortgage,bool_mortgage):
        self.loan_apply_id = loan_apply_id
        self.obj_name = obj_name
        self.owner_address = owner_address
        self.description = description
        self.registration_number = registration_number
        self.appraisal = appraisal
        self.mortgage = mortgage
        self.bool_mortgage = bool_mortgage

    def add(self):
        db.session.add(self)

# 担保信息
class SC_Guarantees(db.Model):
    __tablename__ = 'sc_guarantees' 
    id = db.Column(db.Integer, primary_key=True)
    loan_apply_id=db.Column(db.Integer)
    name = db.Column(db.String(32)) #姓名
    address = db.Column(db.String(256)) #地址
    id_number = db.Column(db.String(32)) #身份证号码
    workunit = db.Column(db.String(256)) #工作单位
    phone = db.Column(db.String(32)) #电话
    relationship = db.Column(db.String(32)) #与申请人关系

    def __init__(self,loan_apply_id,name,address,id_number,
        workunit,phone,relationship):
        self.loan_apply_id = loan_apply_id
        self.name = name
        self.address = address
        self.id_number = id_number
        self.workunit = workunit
        self.phone = phone
        self.relationship = relationship

    def add(self):
        db.session.add(self)

# 财务信息概览
class SC_Financial_Overview(db.Model):
    __tablename__ = 'sc_financial_overview' 
    id = db.Column(db.Integer, primary_key=True)
    loan_apply_id=db.Column(db.Integer)
    current_assets = db.Column(db.String(32)) #流动资产合计(元)
    current_liabilities = db.Column(db.String(32)) #流动负债合计(元)
    bank_deposits = db.Column(db.String(32)) #现金及银行存款(元)
    accounts_payable = db.Column(db.String(32)) #应付账款(元)
    accounts_receivable = db.Column(db.String(32)) #应收账款(元)
    receipts_in_advance = db.Column(db.String(32)) #预收帐款(元)
    prepayments = db.Column(db.String(32)) #预付账款(元)
    short_term_borrowings = db.Column(db.String(32)) #短期借款(元)
    stock = db.Column(db.String(32)) #存货(元)
    long_term_borrowings = db.Column(db.String(32)) #长期借款(元)
    fixed_assets = db.Column(db.String(32)) #固定资产(元)
    total_liabilities = db.Column(db.String(32)) #负债合计(元)
    other_operating_assets = db.Column(db.String(32)) #其他经营资产(元)
    equity = db.Column(db.String(32)) #所有者权益(元)
    total_assets = db.Column(db.String(32)) #资产合计(元)
    liabilities_plus_equity = db.Column(db.String(32)) #负债加权益(元)
    other_non_sheet_assets = db.Column(db.String(32)) #其他非表内资产(元)
    other_non_sheet_liabilities = db.Column(db.String(32)) #其他非表内负债(元)

    average_monthly_turnover = db.Column(db.String(32)) #月均营业额(元)
    average_net_profit = db.Column(db.String(32)) #平均净利润(元)
    average_monthly_disposable_income = db.Column(db.String(32)) #月平均可支配收入(元)
    asset_liability_ratio = db.Column(db.String(32)) #资产负债率%
    current_ratio = db.Column(db.String(32)) #流动比率%
    quick_ratio = db.Column(db.String(32)) #速动比率%
    inventory_turnover_ratio = db.Column(db.String(32)) #存货周转率%
    accounts_receivable_turnover_ratio = db.Column(db.String(32)) #应收账款周转率%
    accounts_payable_turnover_ratio = db.Column(db.String(32)) #应付账款周转率%
    returns_on_capital = db.Column(db.String(32)) #资本回报率%
    gross_margin = db.Column(db.String(32)) #毛利率%
    net_profit_margin = db.Column(db.String(32)) #净利润率%

    def __init__(self,loan_apply_id,current_assets,current_liabilities,bank_deposits,
        accounts_payable,accounts_receivable,receipts_in_advance,prepayments,short_term_borrowings,
        stock,long_term_borrowings,fixed_assets,total_liabilities,other_operating_assets,equity,
        total_assets,liabilities_plus_equity,
        other_non_sheet_assets,other_non_sheet_liabilities,average_monthly_turnover,average_net_profit,
        average_monthly_disposable_income,asset_liability_ratio,current_ratio,quick_ratio,
        inventory_turnover_ratio,accounts_receivable_turnover_ratio,accounts_payable_turnover_ratio,
        returns_on_capital,gross_margin,net_profit_margin):
        self.loan_apply_id = loan_apply_id
        self.current_assets = current_assets
        self.current_liabilities = current_liabilities
        self.bank_deposits = bank_deposits
        self.accounts_payable = accounts_payable
        self.accounts_receivable = accounts_receivable
        self.receipts_in_advance = receipts_in_advance
        self.prepayments = prepayments
        self.short_term_borrowings = short_term_borrowings
        self.stock = stock
        self.long_term_borrowings = long_term_borrowings
        self.fixed_assets = fixed_assets
        self.total_liabilities = total_liabilities
        self.other_operating_assets = other_operating_assets
        self.equity = equity
        self.total_assets = total_assets
        self.liabilities_plus_equity = liabilities_plus_equity
        self.other_non_sheet_assets = other_non_sheet_assets
        self.other_non_sheet_liabilities = other_non_sheet_liabilities
        self.average_monthly_turnover = average_monthly_turnover
        self.average_net_profit = average_net_profit
        self.average_monthly_disposable_income = average_monthly_disposable_income
        self.asset_liability_ratio = asset_liability_ratio
        self.current_ratio = current_ratio
        self.quick_ratio = quick_ratio
        self.inventory_turnover_ratio = inventory_turnover_ratio
        self.accounts_receivable_turnover_ratio = accounts_receivable_turnover_ratio
        self.accounts_payable_turnover_ratio = accounts_payable_turnover_ratio
        self.returns_on_capital = returns_on_capital
        self.gross_margin = gross_margin
        self.net_profit_margin = net_profit_margin

    def add(self):
        db.session.add(self)

# 非财务情况分析
class SC_Non_Financial_Analysis(db.Model):
    __tablename__ = 'sc_non_financial_analysis' 
    id = db.Column(db.Integer, primary_key=True)
    loan_apply_id=db.Column(db.Integer)
    operating_history = db.Column(db.String(256)) #经营历史和资本积累
    structure_and_market = db.Column(db.String(256)) #生意现状：组织架构和市场
    finance = db.Column(db.String(256)) #生意现状：财务
    changes_in_operations_1 = db.Column(db.String(256)) #自从上次申请后经营变化(业务方面)
    changes_in_operations_2 = db.Column(db.String(256)) #自从上次申请后经营变化(私人方面)
    investment_1 = db.Column(db.String(256)) #过去十二个月内的投资情况(业务方面)
    investment_2 = db.Column(db.String(256)) #过去十二个月内的投资情况(私人方面)
    investment_plan_1 = db.Column(db.String(256)) #未来十二个月的投资计划(业务方面)
    investment_plan_2 = db.Column(db.String(256)) #未来十二个月的投资计划(私人方面)
    loan_purpose_detail = db.Column(db.String(256)) #贷款目的的详细描述
    personal_circumstances = db.Column(db.String(256)) #客户/法人/实际经营人/主要股东的私人情况
    impression_of_the_customer = db.Column(db.String(256)) #对客户的印象
    other_sources_of_repayment = db.Column(db.String(256)) #其他还款来源分析

    def __init__(self,loan_apply_id,operating_history,structure_and_market,finance,
        changes_in_operations_1,changes_in_operations_2,
        investment_1,investment_2,
        investment_plan_1,investment_plan_2,
        loan_purpose_detail,personal_circumstances,impression_of_the_customer,other_sources_of_repayment):
        self.loan_apply_id = loan_apply_id
        self.operating_history = operating_history
        self.structure_and_market = structure_and_market
        self.finance = finance
        self.changes_in_operations_1 = changes_in_operations_1
        self.changes_in_operations_2 = changes_in_operations_2
        self.investment_1 = investment_1
        self.investment_2 = investment_2
        self.investment_plan_1 = investment_plan_1
        self.investment_plan_2 = investment_plan_2
        self.loan_purpose_detail = loan_purpose_detail
        self.personal_circumstances = personal_circumstances
        self.impression_of_the_customer = impression_of_the_customer
        self.other_sources_of_repayment = other_sources_of_repayment

    def add(self):
        db.session.add(self)

# 风险分析以及调查结论
class SC_Riskanalysis_And_Findings(db.Model):
    __tablename__ = 'sc_riskanalysis_and_findings' 
    id = db.Column(db.Integer, primary_key=True)
    loan_apply_id=db.Column(db.Integer)
    analysis_conclusion = db.Column(db.String(256)) #分析结论
    amount_recommended = db.Column(db.String(32)) #建议金额(元)
    recommended_deadline = db.Column(db.Date) #建议期限
    recommended_rates = db.Column(db.String(32)) #建议利率
    monthly_repayment_amount = db.Column(db.String(32)) #每月还款额(元)
    recommended_way_of_security = db.Column(db.String(32)) #建议担保方式
    income_ratio = db.Column(db.String(32)) #月付款占可支配收入比重
    survey_signature = db.Column(db.String(32)) #调查人签字
    survey_date = db.Column(db.Date) #日期
    verification = db.Column(db.Integer) #客户信息收集与核实
    others = db.Column(db.String(256)) #其他
    bool_grant = db.Column(db.String(1)) #是否发放(建议)
    amount = db.Column(db.String(32)) #金额(元)
    deadline = db.Column(db.String(32)) #期限
    rates = db.Column(db.String(32)) #利率
    monthly_repayment = db.Column(db.String(32)) #月还款额（元）
    approve_reason = db.Column(db.String(256)) #建议理由/发放条件
    refuse_reason = db.Column(db.String(256)) #否决原因

    other_deliberations=db.Column(db.String(256))#其他审议内容
    positive=db.Column(db.String(256))#正
    opposite=db.Column(db.String(256))#反

    create_user = db.Column(db.Integer)
    create_date = db.Column(db.DateTime)
    modify_user = db.Column(db.Integer)
    modify_date = db.Column(db.DateTime)

    def __init__(self,loan_apply_id,analysis_conclusion,amount_recommended,recommended_deadline,
        recommended_rates,monthly_repayment_amount,recommended_way_of_security,income_ratio,
        survey_signature,survey_date,verification,others,bool_grant,amount,deadline,rates,
        monthly_repayment,approve_reason,refuse_reason,
        other_deliberations,positive,opposite):
        self.loan_apply_id = loan_apply_id
        self.analysis_conclusion = analysis_conclusion
        self.amount_recommended = amount_recommended
        self.recommended_deadline = recommended_deadline
        self.recommended_rates = recommended_rates
        self.monthly_repayment_amount = monthly_repayment_amount
        self.recommended_way_of_security = recommended_way_of_security
        self.income_ratio = income_ratio
        self.survey_signature = survey_signature
        self.survey_date = survey_date
        self.verification = verification
        self.others = others
        self.bool_grant = bool_grant
        self.amount = amount
        self.deadline = deadline
        self.rates = rates
        self.monthly_repayment = monthly_repayment
        self.approve_reason = approve_reason
        self.refuse_reason = refuse_reason
        self.other_deliberations = other_deliberations
        self.positive = positive
        self.opposite = opposite
        self.create_user = current_user.id
        self.create_date = datetime.datetime.now()
        self.modify_user = current_user.id
        self.modify_date = datetime.datetime.now()

    def add(self):
        db.session.add(self)

# 审批决议
class SC_Approval_Decision (db.Model):
    __tablename__ = 'sc_approval_decision' 
    id = db.Column(db.Integer, primary_key=True)
    loan_apply_id=db.Column(db.Integer)
    
    bool_grant = db.Column(db.String(1)) #是否发放(建议)
    amount = db.Column(db.String(32)) #金额(元)
    deadline = db.Column(db.String(32)) #期限
    rates = db.Column(db.String(32)) #利率
    repayment_type = db.Column(db.Integer) #还款方式
    monthly_repayment = db.Column(db.String(32)) #月还款额（元）
    bool_co_borrower = db.Column(db.Integer)#共同借款人
    bool_guaranty = db.Column(db.Integer)#抵质押
    bool_guarantees = db.Column(db.Integer)#保证
    other_resolution = db.Column(db.String(256)) #其他决议内容
    refuse_reason = db.Column(db.String(256)) #否决原因
    conditional_pass = db.Column(db.String(256)) #有条件通过

    loan_date = db.Column(db.Date) #放款日期
    first_repayment_date = db.Column(db.Date) #第一次还贷日期

    management_coats = db.Column(db.String(32)) #管理费(元)
    agency_coats = db.Column(db.String(32)) #代理费(元)
    contract_date = db.Column(db.Date) #合同签订日期
    loan_account = db.Column(db.String(32)) #放款帐号
    bank_customer_no=db.Column(db.String(32)) #银行客户号
    loan_contract_number = db.Column(db.String(32)) #贷款合同编号
    guarantee_contract_number = db.Column(db.String(32)) #担保合同编号
    collateral_contract_number = db.Column(db.String(32)) #抵押品合同编号

    create_user = db.Column(db.Integer)
    create_date = db.Column(db.DateTime)
    modify_user = db.Column(db.Integer)
    modify_date = db.Column(db.DateTime)

    def __init__(self,loan_apply_id,bool_grant,amount,deadline,rates,
        repayment_type,monthly_repayment,bool_co_borrower,bool_guaranty,bool_guarantees,
        other_resolution,refuse_reason,conditional_pass):
        self.loan_apply_id = loan_apply_id
        self.bool_grant = bool_grant
        self.amount = amount
        self.deadline = deadline
        self.rates = rates
        self.repayment_type = repayment_type
        self.monthly_repayment = monthly_repayment
        self.bool_co_borrower = bool_co_borrower
        self.bool_guaranty = bool_guaranty
        self.bool_guarantees = bool_guarantees
        self.other_resolution = other_resolution
        self.refuse_reason = refuse_reason
        self.conditional_pass = conditional_pass
        self.create_user = current_user.id
        self.create_date = datetime.datetime.now()
        self.modify_user = current_user.id
        self.modify_date = datetime.datetime.now()

    def add(self):
        db.session.add(self)

# 上传征信信息表
class SC_Credit_Upload(db.Model):
    __tablename__ = 'sc_credit_upload'
    id=db.Column(db.Integer, primary_key=True)
    loan_apply_id=db.Column(db.Integer)
    info_name=db.Column(db.String(32))
    info_description=db.Column(db.String(128))
    attachment=db.Column(db.String(128))
    create_user = db.Column(db.Integer, db.ForeignKey('sc_user.id')) #上传者
    create_date = db.Column(db.DateTime)
    modify_user = db.Column(db.Integer)
    modify_date = db.Column(db.DateTime)

    # 外键名称
    create_user_name = db.relationship('SC_User',backref = db.backref('create_user_name', lazy = 'dynamic'))

    def __init__(self,loan_apply_id, info_name, info_description, attachment):
        self.loan_apply_id = loan_apply_id
        self.info_name = info_name
        self.info_description = info_description
        self.attachment = attachment
        self.create_user = current_user.id
        self.create_date = datetime.datetime.now()
        self.modify_user = current_user.id
        self.modify_date = datetime.datetime.now()

    def add(self):
        db.session.add(self)

# 标准监测和非标准监测表
class SC_Monitor(db.Model):
    __tablename__ = 'sc_monitor'
    id=db.Column(db.Integer, primary_key=True)
    loan_apply_id=db.Column(db.Integer)
    type = db.Column(db.Integer) #监控类型 1：标准 2：非标准
    monitor_date = db.Column(db.Date) #监控日期
    monitor_officer = db.Column(db.Integer, db.ForeignKey('sc_user.id')) #监控客户经理

    #标准
    monitor_type = db.Column(db.String(32)) #监控方式
    monitor_record = db.Column(db.String(256)) #监控记录
    #非标准
    address = db.Column(db.String(64)) #地点
    related_person = db.Column(db.String(64)) #相关人员
    monitor_reason = db.Column(db.String(256)) #采取非标准监控的原因
    judgement = db.Column(db.String(256)) #非标监控的基本判断
    follow_up_work = db.Column(db.String(256)) #后续重点工作

    create_user = db.Column(db.Integer)
    create_date = db.Column(db.DateTime)
    modify_user = db.Column(db.Integer)
    modify_date = db.Column(db.DateTime)

    # 外键名称
    monitor_officer_name = db.relationship('SC_User',backref = db.backref('monitor_officer_name', lazy = 'dynamic'))

    def __init__(self,loan_apply_id, type, monitor_date,monitor_officer, monitor_type,monitor_record,
        address, related_person, monitor_reason,judgement,follow_up_work):
        self.loan_apply_id = loan_apply_id
        self.type = type
        self.monitor_date = monitor_date
        self.monitor_officer = current_user.id
        self.monitor_type = monitor_type
        self.monitor_record = monitor_record
        self.address = address
        self.related_person = related_person
        self.monitor_reason = monitor_reason
        self.judgement = judgement
        self.follow_up_work = follow_up_work
        self.create_user = current_user.id
        self.create_date = datetime.datetime.now()
        self.modify_user = current_user.id
        self.modify_date = datetime.datetime.now()

    def add(self):
        db.session.add(self)

# 资产分类表
class SC_Classify(db.Model):
    __tablename__ = 'sc_classify'
    id=db.Column(db.Integer, primary_key=True)
    loan_apply_id=db.Column(db.Integer)
    index = db.Column(db.Integer) #递增的序号 从0开始
    classify = db.Column(db.Integer) #等级
    classify_dec = db.Column(db.String(256)) #等级描述
    is_pass = db.Column(db.Integer) #是否通过
    create_user = db.Column(db.Integer)
    create_date = db.Column(db.DateTime)
    confirm_user = db.Column(db.Integer)
    confirm_date = db.Column(db.DateTime)

    def __init__(self,loan_apply_id, index, classify,classify_dec, is_pass):
        self.loan_apply_id = loan_apply_id
        self.index = index
        self.classify = classify
        self.classify_dec = classify_dec
        self.is_pass = is_pass
        self.create_user = current_user.id
        self.create_date = datetime.datetime.now()

    def add(self):
        db.session.add(self)