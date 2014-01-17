#coding:utf-8
__author__ = 'Johnny'

from scapp import db

# 交叉检验
class SC_Cross_Examination(db.Model):
    '''
     交叉检验
    '''
    __tablename__ = 'sc_cross_examination'
    id = db.Column(db.Integer, primary_key=True)
    loan_apply_id=db.Column(db.Integer)
    initial_equity=db.Column(db.String(32))#初始权益
    profit_period=db.Column(db.String(32))#期间利润
    injection_period=db.Column(db.String(32))#期间注资
    pick_period=db.Column(db.String(32))#期内提取资金
    depreciation=db.Column(db.String(32))#折旧
    appreciation=db.Column(db.String(32))#升值
    due_rights=db.Column(db.String(32))#应有权益
    fact_rights=db.Column(db.String(32))#实际权益
    dif_rate=db.Column(db.String(32))#差异率
    right_explanation=db.Column(db.String(64))#权益交叉检验说明
    business_cross=db.Column(db.String(64))#营业额交叉检验
    cost_structure=db.Column(db.String(64))#成本结构分析
    risk_analysis=db.Column(db.String(64))#风险分析对客户优势及对还款能力有威胁的潜在因素的分析

    def __init__(self,loan_apply_id,initial_equity,profit_period,injection_period,pick_period,depreciation,appreciation
                        ,due_rights,fact_rights,dif_rate,right_explanation,business_cross,cost_structure,risk_analysis):
        self.loan_apply_id = loan_apply_id
        self.initial_equity = initial_equity
        self.profit_period = profit_period
        self.injection_period = injection_period
        self.pick_period = pick_period
        self.depreciation = depreciation
        self.appreciation = appreciation
        self.due_rights = due_rights
        self.fact_rights = fact_rights
        self.dif_rate = dif_rate
        self.right_explanation = right_explanation
        self.business_cross = business_cross
        self.cost_structure = cost_structure
        self.risk_analysis = risk_analysis


    def add(self):
        db.session.add(self)