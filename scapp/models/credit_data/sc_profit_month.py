#coding:utf-8
__author__ = 'Johnny'

from scapp import db

# 损益表-月均毛利分析
class SC_Profit_month(db.Model):
    '''
     损益表-月均毛利分析
    '''
    __tablename__ = 'sc_profit_month'
    id = db.Column(db.Integer, primary_key=True)
    loan_apply_id=db.Column(db.Integer)
    project_name=db.Column(db.VARCHAR(64))#项目名称
    purchase_price=db.Column(db.Float(18,2))#进价
    sale_price=db.Column(db.Float(18,2))#售价
    spread=db.Column(db.Float(18,2))#差价
    sales_ratio=db.Column(db.Float(18,2))#销售比例
    gross_profit=db.Column(db.Float(18,2))#毛利率

    def __init__(self,loan_apply_id,project_name,purchase_price,sale_price,spread,sales_ratio,gross_profit):
        self.loan_apply_id = loan_apply_id
        self.project_name = project_name
        self.purchase_price = purchase_price
        self.sale_price = sale_price
        self.spread = spread
        self.sales_ratio = sales_ratio
        self.gross_profit = gross_profit


    def add(self):
        db.session.add(self)