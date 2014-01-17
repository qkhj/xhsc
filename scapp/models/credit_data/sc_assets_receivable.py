#coding:utf-8
__author__ = 'Johnny'


from scapp import db

# 资产负债表-应收账款,预付账款
class SC_Assets_Receivable(db.Model):
    '''
    资产负债表-应收账款,预付账款
    账户类型,0:应收账款，1：预付账款
    '''
    __tablename__ = 'sc_assets_receivable'
    id = db.Column(db.Integer, primary_key=True)
    loan_apply_id=db.Column(db.Integer)
    accounts_type=db.Column(db.CHAR(1))#账户类型,0:应收账款，1：预付账款
    customer_name=db.Column(db.String(64))#应收/预付客户名称
    describe=db.Column(db.String(256))#描述
    proportion=db.Column(db.String(32))#比例
    amount=db.Column(db.String(32))#金额

    def __init__(self,loan_apply_id,accounts_type,customer_name,describe,proportion,amount):
        self.loan_apply_id = loan_apply_id
        self.accounts_type = accounts_type
        self.customer_name = customer_name
        self.describe = describe
        self.proportion = proportion
        self.amount = amount

    def add(self):
        db.session.add(self)