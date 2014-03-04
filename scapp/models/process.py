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
    last_repayment_date  = db.Column(db.Date) #到期日
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
    id = db.Column(db.Integer, primary_key=True)
    loan_apply_id=db.Column(db.Integer)
    monitor_date=db.Column(db.Date)#监控时间
    monitor_type=db.Column(db.String(32))#监控类型
    monitor_content=db.Column(db.String(64))#监控类型
    monitor_remark=db.Column(db.String(256))#备注
    create_user=db.Column(db.Integer)#创建人
    create_date=db.Column(db.Date)#创建时间

    def __init__(self,loan_apply_id,monitor_date,monitor_type,monitor_content,monitor_remark):
        self.loan_apply_id = loan_apply_id
        self.monitor_date = monitor_date
        self.monitor_type = monitor_type
        self.monitor_content = monitor_content
        self.monitor_remark = monitor_remark
        self.create_user = current_user.id
        self.create_date = datetime.datetime.now()

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

# 非标准监测-资产负债表
class SC_Balance_Sheet_Fbz(db.Model):
    __tablename__ = 'sc_balance_sheet_fbz'
    id=db.Column(db.Integer, primary_key=True)
    loan_apply_id=db.Column(db.Integer)
    index = db.Column(db.Integer) #递增的序号 从0开始
    cash_deposit = db.Column(db.String(32)) #现金及存款
    payable = db.Column(db.String(32)) #应付
    receivable = db.Column(db.String(32)) #应收
    short_loan = db.Column(db.String(32)) #短期借款
    stock = db.Column(db.String(32)) #存货
    long_loan = db.Column(db.String(32)) #长期借款
    total_current_assets = db.Column(db.String(32)) #流动资产合计
    total_debt = db.Column(db.String(32)) #负债总计
    total_fixed_assets = db.Column(db.String(32)) #固定资产合计
    owner_equity  = db.Column(db.String(32)) #所有者权益
    total_assets = db.Column(db.String(32)) #资产总计
    debt_and_owner_equity = db.Column(db.String(32)) #负债及所有者权益
    remark = db.Column(db.String(2048)) #对资产负债表的评注
    create_user = db.Column(db.Integer)
    create_date = db.Column(db.DateTime)
    modify_user = db.Column(db.Integer)
    modify_date = db.Column(db.DateTime)

    def __init__(self,loan_apply_id, index, cash_deposit,payable, receivable,short_loan,stock,long_loan,
        total_current_assets,total_debt,total_fixed_assets,owner_equity,total_assets,debt_and_owner_equity,
        remark):
        self.loan_apply_id=loan_apply_id
        self.index = index
        self.cash_deposit = cash_deposit
        self.payable = payable
        self.receivable = receivable
        self.short_loan = short_loan
        self.stock = stock
        self.long_loan = long_loan
        self.total_current_assets = total_current_assets
        self.total_debt = total_debt
        self.total_fixed_assets = total_fixed_assets
        self.owner_equity = owner_equity
        self.total_assets = total_assets
        self.debt_and_owner_equity = debt_and_owner_equity
        self.remark = remark
        self.create_user = current_user.id
        self.create_date = datetime.datetime.now()

    def add(self):
        db.session.add(self)

# 非标准监测-资产负债表
class SC_Profit_Loss_Fbz(db.Model):
    __tablename__ = 'sc_profit_loss_fbz'
    id=db.Column(db.Integer, primary_key=True)
    loan_apply_id=db.Column(db.Integer)
    index = db.Column(db.Integer) #递增的序号 从0开始
    income = db.Column(db.String(32)) #收入
    cost = db.Column(db.String(32)) #变量成本
    gross_profit  = db.Column(db.String(32)) #毛利
    salary = db.Column(db.String(32)) #工资
    insurance = db.Column(db.String(32)) #社会保险
    rent = db.Column(db.String(32)) #租金
    freight = db.Column(db.String(32)) #交通运输费用
    maintain = db.Column(db.String(32)) #维护费用
    utility  = db.Column(db.String(32)) #水电费用
    stock_loss = db.Column(db.String(32)) #存货损失
    taxes = db.Column(db.String(32)) #税金
    others = db.Column(db.String(32)) #其它
    stages = db.Column(db.String(32)) #分期付款
    total_cost = db.Column(db.String(32)) #经营成本总额
    net_profit = db.Column(db.String(32)) #净利润
    other_pay = db.Column(db.String(32)) #家庭及其它支出
    other_income = db.Column(db.String(32)) #其它收入
    family_income = db.Column(db.String(32)) #可供支配的家庭收入
    remark1 = db.Column(db.String(2048)) #remark1
    remark2 = db.Column(db.String(2048)) #remark2

    create_user = db.Column(db.Integer)
    create_date = db.Column(db.DateTime)
    modify_user = db.Column(db.Integer)
    modify_date = db.Column(db.DateTime)

    def __init__(self,loan_apply_id, index,income,cost,gross_profit,salary,insurance,
        rent,freight,maintain,utility,stock_loss,taxes,others,stages,total_cost,net_profit,
        other_pay,other_income,family_income,remark1,remark2):
        self.loan_apply_id=loan_apply_id
        self.index = index
        self.income = income
        self.cost = cost
        self.gross_profit = gross_profit
        self.salary = salary
        self.insurance = insurance
        self.rent = rent
        self.freight = freight
        self.maintain = maintain
        self.utility = utility
        self.stock_loss = stock_loss
        self.taxes = taxes
        self.others = others
        self.stages = stages
        self.total_cost = total_cost
        self.net_profit = net_profit
        self.other_pay = other_pay
        self.other_income = other_income
        self.family_income = family_income
        self.remark1 = remark1
        self.remark2 = remark2
        self.create_user = current_user.id
        self.create_date = datetime.datetime.now()

    def add(self):
        db.session.add(self)