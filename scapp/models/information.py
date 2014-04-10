#coding:utf-8
from flask.ext.login import current_user

from scapp import db

import datetime
import json

# 目标客户表
class SC_Target_Customer(db.Model):
    __tablename__ = 'sc_target_customer' 
    id = db.Column(db.Integer, primary_key=True)
    receiver = db.Column(db.Integer, db.ForeignKey('sc_user.id')) # 接待人
    reception_type = db.Column(db.String(1)) #接待方式 (咨询 0/扫街 1)

    yingxiao_status = db.Column(db.Integer) # 营销状态
    client_status = db.Column(db.Integer) # 客户状态
    is_apply_form = db.Column(db.Integer) # 是否向小微支行填写申请表？

    customer_name = db.Column(db.String(32)) #客户名称
    mobile = db.Column(db.String(16)) #电话
    sex = db.Column(db.String(1)) #性别
    age = db.Column(db.String(8)) #年龄
    address = db.Column(db.String(128)) #地址
    industry = db.Column(db.Integer, db.ForeignKey('sc_industry.id')) #所属行业
    business_content = db.Column(db.String(256)) #经营内容

    shop_name = db.Column(db.String(128)) #店铺名称
    period = db.Column(db.String(8)) #经营期限
    property_scope = db.Column(db.String(16)) #资产规模(数字)
    monthly_sales = db.Column(db.String(16)) #月销售额
    employees = db.Column(db.String(16)) #雇员数量
    business_type = db.Column(db.Integer, db.ForeignKey('sc_business_type.id')) #企业类别

    is_need_loan = db.Column(db.String(256)) #是否有贷款需求

    loan_purpose = db.Column(db.Integer, db.ForeignKey('sc_loan_purpose.id')) #贷款目的
    loan_amount = db.Column(db.String(16)) #贷款数额
    repayment_type = db.Column(db.String(64)) #希望的还款方式
    guarantee_type = db.Column(db.String(64)) #能提供的担保方式
    house_property = db.Column(db.String(64)) #房产产权情况
    loan_attention = db.Column(db.String(64)) #贷款关注程度

    is_have_loan = db.Column(db.String(1)) #是否在银行贷过款
    is_known_xhnsh = db.Column(db.String(1)) #知道兴化农商行吗？
    business_with_xhnsh = db.Column(db.String(256)) #您在兴化农村商业银行办理过什么业务？
    is_need_service = db.Column(db.String(1)) #您是否需要办理以下银行产品

    status = db.Column(db.Integer) #状态
    manager = db.Column(db.Integer, db.ForeignKey('sc_user.id')) #分配主管
    loan_officer = db.Column(db.Integer, db.ForeignKey('sc_user.id')) #分配客户经理
    loan_officer_date = db.Column(db.DateTime)

    bool_regisiter = db.Column(db.Integer) #已录入
    remark = db.Column(db.String(256)) #备注
    create_user = db.Column(db.Integer)
    create_date = db.Column(db.DateTime)
    modify_user = db.Column(db.Integer)
    modify_date = db.Column(db.DateTime)

    # 外键名称
    receiver_for_tc = db.relationship('SC_User',foreign_keys=[receiver], backref = db.backref('receiver_for_tc', lazy = 'dynamic'))
    # 外键名称
    manager_for_tc = db.relationship('SC_User',foreign_keys=[manager], backref = db.backref('manager_for_tc', lazy = 'dynamic'))
    # 外键名称
    loan_officer_for_tc = db.relationship('SC_User',foreign_keys=[loan_officer], backref = db.backref('loan_officer_for_tc', lazy = 'dynamic'))
    # 外键名称
    industry_type_name_for_tc = db.relationship('SC_Industry', backref = db.backref('industry_type_name_for_tc', lazy = 'dynamic'))
    # 外键名称
    business_type_name_for_tc = db.relationship('SC_Business_Type', backref = db.backref('business_type_name_for_tc', lazy = 'dynamic'))
    # 外键名称
    loan_purpose_name_for_tc = db.relationship('SC_Loan_Purpose', backref = db.backref('loan_purpose_name_for_tc', lazy = 'dynamic'))

    def __init__(self,receiver,reception_type,yingxiao_status,client_status,is_apply_form,
        customer_name,mobile,sex,age,address,industry,business_content,
        shop_name,period,property_scope,monthly_sales,employees,business_type,is_need_loan,loan_purpose,
        loan_amount,repayment_type,guarantee_type,house_property,loan_attention,is_have_loan,is_known_xhnsh,
        business_with_xhnsh,is_need_service,status,manager,loan_officer,loan_officer_date,bool_regisiter,remark):
        self.receiver = receiver
        self.reception_type = reception_type
        self.yingxiao_status = yingxiao_status
        self.client_status = client_status
        self.is_apply_form = is_apply_form
        self.customer_name = customer_name
        self.mobile = mobile
        self.sex = sex
        self.age = age
        self.address = address
        self.industry = industry
        self.business_content = business_content
        self.shop_name = shop_name
        self.period = period
        self.property_scope = property_scope
        self.monthly_sales = monthly_sales
        self.employees = employees
        self.business_type = business_type
        self.is_need_loan = is_need_loan
        self.loan_purpose = loan_purpose
        self.loan_amount = loan_amount
        self.repayment_type = repayment_type
        self.guarantee_type = guarantee_type
        self.house_property = house_property
        self.loan_attention = loan_attention
        self.is_have_loan = is_have_loan
        self.is_known_xhnsh = is_known_xhnsh
        self.business_with_xhnsh = business_with_xhnsh
        self.is_need_service = is_need_service
        self.status = status
        self.manager = manager
        self.loan_officer = loan_officer
        self.bool_regisiter = bool_regisiter
        self.loan_officer_date = loan_officer_date
        self.remark = remark
        self.create_user = current_user.id
        self.create_date = datetime.datetime.now()
        self.modify_user = current_user.id
        self.modify_date = datetime.datetime.now()

    def add(self):
        db.session.add(self)

# 个人客户基本信息表
class SC_Individual_Customer(db.Model):
    __tablename__ = 'sc_individual_customer'
    id=db.Column(db.Integer, primary_key=True)
    manager=db.Column(db.Integer, db.ForeignKey('sc_user.id'))
    customer_no=db.Column(db.String(16))
    customer_type=db.Column(db.String(16))
    customer_name=db.Column(db.String(128))
    birthday=db.Column(db.Date)
    sex=db.Column(db.String(1))
    credentials_type=db.Column(db.Integer, db.ForeignKey('sc_credentials_type.id'))
    credentials_no=db.Column(db.String(32))
    degree=db.Column(db.String(32))
    education=db.Column(db.String(32))
    marriage=db.Column(db.String(1))
    telephone=db.Column(db.String(16))
    mobile=db.Column(db.String(16))
    residence=db.Column(db.String(128))
    residence_address=db.Column(db.String(128))
    home_address=db.Column(db.String(128))
    zip_code=db.Column(db.String(16))
    families=db.Column(db.String(2))
    living_conditions=db.Column(db.String(32))
    is_otherjob=db.Column(db.String(1))
    profession=db.Column(db.String(64))
    duty=db.Column(db.String(64))
    title=db.Column(db.String(64))
    name_1=db.Column(db.String(64))
    relationship_1=db.Column(db.String(64))
    phone_1=db.Column(db.String(64))
    name_2=db.Column(db.String(64))
    relationship_2=db.Column(db.String(64))
    phone_2=db.Column(db.String(64))
    name_3=db.Column(db.String(64))
    relationship_3=db.Column(db.String(64))
    phone_3=db.Column(db.String(64))
    name_4=db.Column(db.String(64))
    relationship_4=db.Column(db.String(64))
    phone_4=db.Column(db.String(64))
    spouse_name=db.Column(db.String(32))
    spouse_company=db.Column(db.String(64))
    spouse_credentials_type=db.Column(db.Integer, db.ForeignKey('sc_credentials_type.id'))
    spouse_credentials_no=db.Column(db.String(32))
    spouse_phone=db.Column(db.String(32))
    spouse_mobile=db.Column(db.String(32))
    is_active = db.Column(db.String(1))
    is_have_export = db.Column(db.String(1))
    create_user = db.Column(db.Integer)
    create_date = db.Column(db.DateTime)
    modify_user = db.Column(db.Integer)
    modify_date = db.Column(db.DateTime)

    # 外键名称
    user_for_individual = db.relationship('SC_User', backref = db.backref('user_for_individual', lazy = 'dynamic'))
    # 外键名称
    credentials_name = db.relationship('SC_Credentials_Type',foreign_keys=[credentials_type], backref = db.backref('credentials_name', lazy = 'dynamic'))
    # 外键名称
    spouse_credentials_name = db.relationship('SC_Credentials_Type',foreign_keys=[spouse_credentials_type], backref = db.backref('spouse_credentials_name', lazy = 'dynamic'))

    def __init__(self, manager,customer_no,customer_name,birthday,sex,credentials_type,credentials_no,
                degree,education,marriage,telephone,mobile,residence,residence_address,home_address,
                zip_code,families,living_conditions,is_otherjob,profession,duty,title,
                name_1,relationship_1,phone_1,name_2,relationship_2,phone_2,
                name_3,relationship_3,phone_3,name_4,relationship_4,phone_4,
                spouse_name,spouse_company,spouse_credentials_type,spouse_credentials_no,spouse_phone,spouse_mobile):
        self.manager=manager
        self.customer_no=customer_no
        self.customer_type='Individual'
        self.customer_name=customer_name
        self.birthday=birthday
        self.sex=sex
        self.credentials_type=credentials_type
        self.credentials_no=credentials_no
        self.degree=degree
        self.education=education
        self.marriage=marriage
        self.telephone=telephone
        self.mobile=mobile
        self.residence=residence
        self.residence_address=residence_address
        self.home_address=home_address
        self.zip_code=zip_code
        self.families=families
        self.living_conditions=living_conditions
        self.is_otherjob=is_otherjob
        self.profession=profession
        self.duty=duty
        self.title=title
        self.name_1=name_1
        self.relationship_1=relationship_1
        self.phone_1=phone_1
        self.name_2=name_2
        self.relationship_2=relationship_2
        self.phone_2=phone_2
        self.name_3=name_3
        self.relationship_3=relationship_3
        self.phone_3=phone_3
        self.name_4=name_4
        self.relationship_4=relationship_4
        self.phone_4=phone_4
        self.spouse_name=spouse_name
        self.spouse_company=spouse_company
        self.spouse_credentials_type=spouse_credentials_type
        self.spouse_credentials_no=spouse_credentials_no
        self.spouse_phone=spouse_phone
        self.spouse_mobile=spouse_mobile
        self.is_active = '1'
        self.is_have_export = '0'
        self.create_user = current_user.id
        self.create_date = datetime.datetime.now()
        self.modify_user = current_user.id
        self.modify_date = datetime.datetime.now()

    def add(self):
        db.session.add(self)

# 业务往来表
class SC_Dealings(db.Model):
    __tablename__ = 'sc_dealings'
    id=db.Column(db.Integer, primary_key=True)
    deal_name=db.Column(db.String(32))
    deal_description=db.Column(db.String(128))
    belong_customer_type=db.Column(db.String(16))
    belong_customer_value=db.Column(db.Integer)
    create_user = db.Column(db.Integer)
    create_date = db.Column(db.DateTime)
    modify_user = db.Column(db.Integer)
    modify_date = db.Column(db.DateTime)

    def __init__(self, deal_name, deal_description, belong_customer_type, belong_customer_value):
        self.deal_name = deal_name
        self.deal_description = deal_description
        self.belong_customer_type = belong_customer_type
        self.belong_customer_value = belong_customer_value
        self.create_user = current_user.id
        self.create_date = datetime.datetime.now()
        self.modify_user = current_user.id
        self.modify_date = datetime.datetime.now()

    def add(self):
        db.session.add(self)

# 证件类型表
class SC_Credentials_Type(db.Model):
    __tablename__ = 'sc_credentials_type'
    id=db.Column(db.Integer, primary_key=True)
    type_name=db.Column(db.String(16))

    def __init__(self, type_name):
        self.type_name = type_name

    def add(self):
        db.session.add(self)

# 公司客户基本表
class SC_Company_Customer(db.Model):
    __tablename__ = 'sc_company_customer'
    id=db.Column(db.Integer, primary_key=True)
    manager=db.Column(db.Integer, db.ForeignKey('sc_user.id'))
    customer_no=db.Column(db.String(16))
    customer_name=db.Column(db.String(128))
    customer_type=db.Column(db.String(16))
    frdb=db.Column(db.String(32))
    yyzz=db.Column(db.String(32))
    yyzz_fzjg=db.Column(db.String(64))
    swdjz=db.Column(db.String(32))
    swdjz_fzjg=db.Column(db.String(64))
    gszczj=db.Column(db.Integer)
    gsyyfw=db.Column(db.String(128))
    gsclrq=db.Column(db.Date)
    gszclx=db.Column(db.Integer, db.ForeignKey('sc_regisiter_type.id'))
    jbhzh=db.Column(db.String(32))
    zcdz=db.Column(db.String(128))
    xdz=db.Column(db.String(128))
    bgdz=db.Column(db.String(128))
    qtdz=db.Column(db.String(128))
    education=db.Column(db.String(32))
    family=db.Column(db.String(256))
    telephone=db.Column(db.String(16))
    mobile=db.Column(db.String(16))
    contact_phone=db.Column(db.String(16))
    email=db.Column(db.String(32))
    is_active=db.Column(db.String(1))
    create_user = db.Column(db.Integer)
    create_date = db.Column(db.DateTime)
    modify_user = db.Column(db.Integer)
    modify_date = db.Column(db.DateTime)

    # 外键名称
    user_for_company = db.relationship('SC_User', backref = db.backref('user_for_company', lazy = 'dynamic'))
    # 外键名称
    regisiter_type = db.relationship('SC_Regisiter_Type', backref = db.backref('regisiter_type', lazy = 'dynamic'))
    
    def __init__(self, manager,customer_no,customer_name,frdb,yyzz,yyzz_fzjg,swdjz,swdjz_fzjg,
                gszczj,gsyyfw,gsclrq,gszclx,jbhzh,zcdz,xdz,bgdz,
                qtdz,education,family,telephone,mobile,contact_phone,email):
        self.manager = manager
        self.customer_no = customer_no
        self.customer_type = 'Company'
        self.customer_name = customer_name
        self.frdb = frdb
        self.yyzz = yyzz
        self.yyzz_fzjg = yyzz_fzjg
        self.swdjz = swdjz
        self.swdjz_fzjg = swdjz_fzjg
        self.gszczj = gszczj
        self.gsyyfw = gsyyfw
        self.gsclrq = gsclrq
        self.gszclx = gszclx
        self.jbhzh = jbhzh
        self.zcdz = zcdz
        self.xdz = xdz
        self.bgdz = bgdz
        self.qtdz = qtdz
        self.education = education
        self.family = family
        self.telephone = telephone
        self.mobile = mobile
        self.contact_phone = contact_phone
        self.email = email
        self.create_user = current_user.id
        self.create_date = datetime.datetime.now()
        self.modify_user = current_user.id
        self.modify_date = datetime.datetime.now()

    def add(self):
        db.session.add(self)

# 关系人信息表
class SC_Relations(db.Model):
    __tablename__ = 'sc_relations'
    id=db.Column(db.Integer, primary_key=True)
    relation_no=db.Column(db.String(16))
    relation_name=db.Column(db.String(32))
    relation_type=db.Column(db.Integer, db.ForeignKey('sc_relation_type.id'))
    cgbl=db.Column(db.Float)
    business_name=db.Column(db.String(128))
    relation_describe=db.Column(db.String(128))
    belong_customer_type=db.Column(db.String(16))
    belong_customer_value=db.Column(db.Integer)
    create_user = db.Column(db.Integer)
    create_date = db.Column(db.DateTime)
    modify_user = db.Column(db.Integer)
    modify_date = db.Column(db.DateTime)

    # 外键名称
    relation_type_name = db.relationship('SC_Relation_Type', backref = db.backref('relation_type_name', lazy = 'dynamic'))

    def __init__(self, relation_no, relation_name, relation_type, cgbl, business_name, relation_describe,
        belong_customer_type, belong_customer_value):
        self.relation_no = relation_no
        self.relation_name = relation_name
        self.relation_type = relation_type
        self.cgbl = cgbl
        self.business_name = business_name
        self.relation_describe = relation_describe
        self.belong_customer_type = belong_customer_type
        self.belong_customer_value = belong_customer_value
        self.create_user = current_user.id
        self.create_date = datetime.datetime.now()
        self.modify_user = current_user.id
        self.modify_date = datetime.datetime.now()

    def add(self):
        db.session.add(self)

# 关系类型表
class SC_Relation_Type(db.Model):
    __tablename__ = 'sc_relation_type'
    id=db.Column(db.Integer, primary_key=True)
    type_name=db.Column(db.String(16))

    def __init__(self, type_name):
        self.type_name = type_name

    def add(self):
        db.session.add(self)

# 经营信息表
class SC_Manage_Info(db.Model):
    __tablename__ = 'sc_manage_info'
    id=db.Column(db.Integer, primary_key=True)
    business_name=db.Column(db.String(32))
    industry=db.Column(db.Integer, db.ForeignKey('sc_industry.id'))
    business_description=db.Column(db.String(128))
    business_type=db.Column(db.Integer, db.ForeignKey('sc_business_type.id'))
    stake=db.Column(db.String(4))
    business_address=db.Column(db.String(128))
    annual_income=db.Column(db.String(16))
    monthly_income=db.Column(db.String(16))
    establish_date=db.Column(db.Date)
    employees=db.Column(db.String(16))
    manager_name=db.Column(db.String(32))
    credentials_type=db.Column(db.Integer, db.ForeignKey('sc_credentials_type.id'))
    credentials_no=db.Column(db.String(32))
    credentials_org=db.Column(db.String(64))
    belong_customer_type=db.Column(db.String(16))
    belong_customer_value=db.Column(db.Integer)
    create_user = db.Column(db.Integer)
    create_date = db.Column(db.DateTime)
    modify_user = db.Column(db.Integer)
    modify_date = db.Column(db.DateTime)

    # 外键名称
    industry_type_name = db.relationship('SC_Industry', backref = db.backref('industry_type_name', lazy = 'dynamic'))
    # 外键名称
    business_type_name = db.relationship('SC_Business_Type', backref = db.backref('business_type_name', lazy = 'dynamic'))
    # 外键名称
    credentials_type_name = db.relationship('SC_Credentials_Type', backref = db.backref('credentials_type_name', lazy = 'dynamic'))

    def __init__(self, business_name, industry, business_description, business_type,
        stake, business_address, annual_income, monthly_income,
        establish_date, employees, manager_name, credentials_type,
        credentials_no, credentials_org,belong_customer_type,belong_customer_value):
        self.business_name = business_name
        self.industry = industry
        self.business_description = business_description
        self.business_type = business_type
        self.stake = stake
        self.business_address = business_address
        self.annual_income = annual_income
        self.monthly_income = monthly_income
        self.establish_date = establish_date
        self.employees = employees
        self.manager_name = manager_name
        self.credentials_type = credentials_type
        self.credentials_no = credentials_no
        self.credentials_org = credentials_org
        self.belong_customer_type = belong_customer_type
        self.belong_customer_value = belong_customer_value
        self.create_user = current_user.id
        self.create_date = datetime.datetime.now()
        self.modify_user = current_user.id
        self.modify_date = datetime.datetime.now()

    def add(self):
        db.session.add(self)

# 所属行业表
class SC_Industry(db.Model):
    __tablename__ = 'sc_industry'
    id=db.Column(db.Integer, primary_key=True)
    type_name=db.Column(db.String(32))

    def __init__(self, type_name):
        self.type_name = type_name

    def add(self):
        db.session.add(self)

# 资产信息表
class SC_Asset_Info(db.Model):
    __tablename__ = 'sc_asset_info'
    id=db.Column(db.Integer, primary_key=True)
    asset_name=db.Column(db.String(32))
    asset_type=db.Column(db.Integer, db.ForeignKey('sc_asset_type.id'))
    asset_description=db.Column(db.String(128))
    asset_position=db.Column(db.String(128))
    credentials_name=db.Column(db.String(32))
    credentials_no=db.Column(db.String(64))
    appraisal=db.Column(db.DECIMAL(18,2))
    is_mortgage=db.Column(db.String(1))
    mortgage_amount=db.Column(db.DECIMAL(18,2))
    mortgage_object=db.Column(db.String(32))
    belong_customer_type=db.Column(db.String(16))
    belong_customer_value=db.Column(db.Integer)
    create_user = db.Column(db.Integer)
    create_date = db.Column(db.DateTime)
    modify_user = db.Column(db.Integer)
    modify_date = db.Column(db.DateTime)

    # 外键名称
    asset_type_name = db.relationship('SC_Asset_Type', backref = db.backref('asset_type_name', lazy = 'dynamic'))

    def __init__(self, asset_name, asset_type, asset_description, asset_position,
        credentials_name,credentials_no, appraisal, is_mortgage, mortgage_amount,
        mortgage_object,belong_customer_type,belong_customer_value):
        self.asset_name = asset_name
        self.asset_type = asset_type
        self.asset_description = asset_description
        self.asset_position = asset_position
        self.credentials_name = credentials_name
        self.credentials_no = credentials_no
        self.appraisal = appraisal
        self.is_mortgage = is_mortgage
        self.mortgage_amount = mortgage_amount
        self.mortgage_object = mortgage_object
        self.belong_customer_type = belong_customer_type
        self.belong_customer_value = belong_customer_value
        self.create_user = current_user.id
        self.create_date = datetime.datetime.now()
        self.modify_user = current_user.id
        self.modify_date = datetime.datetime.now()

    def add(self):
        db.session.add(self)

# 财务信息表
class SC_Financial_Affairs(db.Model):
    __tablename__ = 'sc_financial_affairs'
    id=db.Column(db.Integer, primary_key=True)
    main_supplier=db.Column(db.String(128))
    main_client=db.Column(db.String(128))
    total_assets=db.Column(db.String(128))
    stock=db.Column(db.String(128))
    accounts=db.Column(db.String(128))
    fixed_assets=db.Column(db.String(128))
    total_liabilities=db.Column(db.String(128))
    bank_borrowings=db.Column(db.String(128))
    private_borrowers=db.Column(db.String(128))
    monthly_sales=db.Column(db.String(128))
    profit=db.Column(db.String(128))
    other_monthly_income=db.Column(db.String(128))
    belong_customer_type=db.Column(db.String(16))
    belong_customer_value=db.Column(db.Integer)
    create_user = db.Column(db.Integer)
    create_date = db.Column(db.DateTime)
    modify_user = db.Column(db.Integer)
    modify_date = db.Column(db.DateTime)

    def __init__(self,
        main_supplier, main_client, total_assets,
        stock, accounts,fixed_assets,
        total_liabilities, bank_borrowings,private_borrowers,
        monthly_sales, profit, other_monthly_income,
        belong_customer_type,belong_customer_value,):
        self.main_supplier = main_supplier
        self.main_client = main_client
        self.total_assets = total_assets
        self.stock = stock
        self.accounts = accounts
        self.fixed_assets = fixed_assets
        self.total_liabilities = total_liabilities
        self.bank_borrowings = bank_borrowings
        self.private_borrowers = private_borrowers
        self.monthly_sales = monthly_sales
        self.profit = profit
        self.other_monthly_income = other_monthly_income
        self.belong_customer_type = belong_customer_type
        self.belong_customer_value = belong_customer_value
        self.create_user = current_user.id
        self.create_date = datetime.datetime.now()
        self.modify_user = current_user.id
        self.modify_date = datetime.datetime.now()

    def add(self):
        db.session.add(self)

# 其他信息表
class SC_Other_Info(db.Model):
    __tablename__ = 'sc_other_info'
    id=db.Column(db.Integer, primary_key=True)
    info_name=db.Column(db.String(32))
    info_description=db.Column(db.String(128))
    attachment=db.Column(db.String(128))
    belong_customer_type=db.Column(db.String(16))
    belong_customer_value=db.Column(db.Integer)
    create_user = db.Column(db.Integer)
    create_date = db.Column(db.DateTime)
    modify_user = db.Column(db.Integer)
    modify_date = db.Column(db.DateTime)

    def __init__(self, info_name, info_description, attachment,
        belong_customer_type,belong_customer_value):
        self.info_name = info_name
        self.info_description = info_description
        self.attachment = attachment
        self.belong_customer_type = belong_customer_type
        self.belong_customer_value = belong_customer_value
        self.create_user = current_user.id
        self.create_date = datetime.datetime.now()
        self.modify_user = current_user.id
        self.modify_date = datetime.datetime.now()

    def add(self):
        db.session.add(self)

# 注册类型表
class SC_Regisiter_Type(db.Model):
    __tablename__ = 'sc_regisiter_type'
    id=db.Column(db.Integer, primary_key=True)
    type_name=db.Column(db.String(16))

    def __init__(self, type_name):
        self.type_name = type_name

    def add(self):
        db.session.add(self)

# 经营性质表
class SC_Business_Type(db.Model):
    __tablename__ = 'sc_business_type'
    id=db.Column(db.Integer, primary_key=True)
    type_name=db.Column(db.String(16))

    def __init__(self, type_name):
        self.type_name = type_name

    def add(self):
        db.session.add(self)

# 资产类型表
class SC_Asset_Type(db.Model):
    __tablename__ = 'sc_asset_type'
    id=db.Column(db.Integer, primary_key=True)
    type_name=db.Column(db.String(16))

    def __init__(self, type_name):
        self.type_name = type_name
        
    def add(self):
        db.session.add(self)
        
# 贷款用途 loan
class SC_Loan_Purpose(db.Model):
    __tablename__ = 'sc_loan_purpose'
    id=db.Column(db.Integer, primary_key=True)
    type_name=db.Column(db.String(16))

    def __init__(self, type_name):
        self.type_name = type_name
        
    def add(self):
        db.session.add(self)

# 风险系数
class SC_Risk_Level(db.Model):
    __tablename__ = 'sc_risk_level'
    id=db.Column(db.Integer, primary_key=True)
    type_name=db.Column(db.String(64))
    type_value=db.Column(db.String(16))

    def __init__(self, type_name,type_value):
        self.type_name = type_name
        self.type_value = type_value
        
    def add(self):
        db.session.add(self)