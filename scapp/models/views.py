#coding:utf-8
from scapp import db

# 获取贷款信息
class View_Query_Loan(db.Model):
    __tablename__ = 'view_query_loan'
    loan_apply_id = db.Column(db.Integer, primary_key=True)
    company_customer_id = db.Column(db.Integer)
    company_customer_no = db.Column(db.Integer)
    company_customer_name = db.Column(db.String)
    company_customer_type = db.Column(db.String)
    individual_customer_id = db.Column(db.Integer)
    individual_customer_no = db.Column(db.Integer)
    individual_customer_name = db.Column(db.String)
    individual_customer_type = db.Column(db.String)
    loan_type = db.Column(db.String)
    loan_amount = db.Column(db.String)#申请金额
    loan_deadline = db.Column(db.Integer)#申请期数
    process_status = db.Column(db.String)
    create_date = db.Column(db.DateTime)#申请时间
    marketing_loan_officer = db.Column(db.Integer, db.ForeignKey('sc_user.id')) #营销信贷员
    A_loan_officer = db.Column(db.Integer)
    B_loan_officer = db.Column(db.Integer)
    yunying_loan_officer = db.Column(db.Integer)
    examiner_1 = db.Column(db.Integer)
    examiner_2 = db.Column(db.Integer)
    approver = db.Column(db.Integer)
    classify = db.Column(db.Integer)
    is_pass = db.Column(db.String)
    amount = db.Column(db.Integer)#审批金额
    deadline = db.Column(db.Integer)#审批期数
    repayment_type = db.Column(db.Integer)#还款方式
    loan_date = db.Column(db.Date)#放款日期
    rates = db.Column(db.String)#利率
    first_repayment_date = db.Column(db.Date)#第一次还款日期

    # 外键名称
    #view_marketing_loan_officer_name = db.relationship('SC_User',backref = db.backref('view_marketing_loan_officer_name', lazy = 'dynamic'))

# 获取用户及用户级别
class View_Get_Cus_Mgr(db.Model):
    __tablename__ = 'view_get_cus_mgr'
    id = db.Column(db.Integer, primary_key=True)
    role_level = db.Column(db.Integer)
    login_name = db.Column(db.String)
    real_name = db.Column(db.String)
    department = db.Column(db.Integer)

# 获取还款记录
class View_Loan_Repayment(db.Model):
    __tablename__ = 'view_loan_repayment'
    id = db.Column(db.Integer, primary_key=True)
    repayment_date = db.Column(db.Date)#实际还款日期
    customer_name = db.Column(db.String)
    total_repayment = db.Column(db.String)#当期实际还款总额
    status = db.Column(db.Integer)#本期还款状态
    principal = db.Column(db.DECIMAL(18,2))#本期本金
    interest = db.Column(db.DECIMAL(18,2))#本期利息
    re_principal = db.Column(db.DECIMAL(18,2))#当期本金剩余
    re_interest = db.Column(db.DECIMAL(18,2))#当期利息剩余
    re_penalty_interest = db.Column(db.DECIMAL(18,2))#当期罚息剩余
    installments = db.Column(db.Integer)#期数
    ratio = db.Column(db.String)#利率
    loan_status = db.Column(db.String)#贷款状态
    loan_manager = db.Column(db.String)#客户经理

# 已发放贷款
class View_Loan_Disbursed(db.Model):
    __tablename__ = 'view_loan_disbursed'
    id = db.Column(db.Integer, primary_key=True)
    loan_type = db.Column(db.Integer)
    customer_name = db.Column(db.String)
    amount = db.Column(db.String)#贷款数额
    ratio = db.Column(db.String)#利率
    lending_date = db.Column(db.Date)#放款日期
    loan_status = db.Column(db.String)#贷款状态
    loan_manager = db.Column(db.String)#客户经理

