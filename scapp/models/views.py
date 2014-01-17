#coding:utf-8
from scapp import db
        
# 贷款用途 loan
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
    loan_amount = db.Column(db.String)
    process_status = db.Column(db.String)
    create_date = db.Column(db.DateTime)
    marketing_loan_officer = db.Column(db.Integer, db.ForeignKey('sc_user.id')) #营销信贷员
    A_loan_officer = db.Column(db.Integer)
    B_loan_officer = db.Column(db.Integer)
    yunying_loan_officer = db.Column(db.Integer)
    examiner_1 = db.Column(db.Integer)
    examiner_2 = db.Column(db.Integer)
    approver = db.Column(db.Integer)

    # 外键名称
    #view_marketing_loan_officer_name = db.relationship('SC_User',backref = db.backref('view_marketing_loan_officer_name', lazy = 'dynamic'))