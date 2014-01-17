#coding:utf-8

from scapp import db

# 现金流分析表
class SC_Cash_Flow(db.Model):
    __tablename__ = 'sc_cash_flow'
    id = db.Column(db.Integer, primary_key=True)
    loan_apply_id=db.Column(db.Integer)
    type=db.Column(db.CHAR(1))#业务类型 0：业务历史1：业务展望
    month=db.Column(db.String(3))#月数
    early_cash=db.Column(db.String(16))#月初现金
    sale_amount = db.Column(db.String(16)) #现金销售额
    accounts_receivable = db.Column(db.String(16)) #应收账款回收
    prepaments = db.Column(db.String(16)) #客户预付款
    total_cash_flow = db.Column(db.String(16)) #经营现金流入总额
    cash_purchase = db.Column(db.String(16)) #现金购买原材料等
    accounts_payable= db.Column(db.String(16)) #应付账款的支付
    advance_purchases = db.Column(db.String(16)) #购货预付款
    total_cash_outflow = db.Column(db.String(16)) #经营现金流出总额
    wage_labor = db.Column(db.String(16)) #工资及劳保
    tax = db.Column(db.String(16)) #税收
    transportation_costs = db.Column(db.String(16)) #交通费用
    rent = db.Column(db.String(16)) #租金
    maintenance_fees = db.Column(db.String(16)) #维护费
    utility_bills = db.Column(db.String(16)) #水电费
    advertising_fees = db.Column(db.String(16)) #广告费
    social_intercourse_fees = db.Column(db.String(16)) #交际费
    fixed_costs=db.Column(db.String(16)) #固定成本
    fixed_asset_investment=db.Column(db.String(16)) #固定资产投资
    disposal_of_fixed_assets=db.Column(db.String(16)) #固定资产出售
    investment_cash_flow=db.Column(db.String(16)) #投资总现金流
    bank_loans=db.Column(db.String(16)) #银行贷款
    repayments_bank=db.Column(db.String(16)) #偿还银行本金及利息
    financing_cash_flow=db.Column(db.String(16)) #融资总现金流
    household_expenditure=db.Column(db.String(16)) #家庭开支
    private_use=db.Column(db.String(16)) #私人使用资金
    private_cash_flow=db.Column(db.String(16))#私人现金流总额
    ljxj = db.Column(db.String(16))#累计现金
    qmxj = db.Column(db.String(16))#期末现金
	
    def __init__(self,loan_apply_id,type,month,early_cash,sale_amount,
                 accounts_receivable,prepaments,total_cash_flow,cash_purchase,accounts_payable,
                 advance_purchases,total_cash_outflow,wage_labor,tax,transportation_costs,rent,maintenance_fees,
                 utility_bills,advertising_fees,social_intercourse_fees,fixed_costs,fixed_asset_investment,disposal_of_fixed_assets,
                 investment_cash_flow,bank_loans,repayments_bank,financing_cash_flow,household_expenditure,private_use,private_cash_flow,
                 ljxj,qmxj):
        self.loan_apply_id = loan_apply_id
        self.type = type
        self.month = month
        self.early_cash = early_cash
        self.sale_amount = sale_amount
        self.accounts_receivable = accounts_receivable
        self.prepaments = prepaments
        self.total_cash_flow = total_cash_flow
        self.cash_purchase = cash_purchase
        self.accounts_payable = accounts_payable
        self.advance_purchases = advance_purchases
        self.total_cash_outflow = total_cash_outflow
        self.wage_labor = wage_labor
        self.tax = tax
        self.transportation_costs = transportation_costs
        self.rent = rent
        self.maintenance_fees = maintenance_fees
        self.utility_bills = utility_bills
        self.advertising_fees = advertising_fees
        self.social_intercourse_fees = social_intercourse_fees
        self.fixed_asset_investment = fixed_asset_investment
        self.fixed_costs = fixed_costs
        self.disposal_of_fixed_assets = disposal_of_fixed_assets
        self.investment_cash_flow = investment_cash_flow
        self.bank_loans = bank_loans
        self.repayments_bank = repayments_bank
        self.financing_cash_flow = financing_cash_flow
        self.household_expenditure = household_expenditure
        self.private_use = private_use
        self.private_cash_flow = private_cash_flow
        self.ljxj = ljxj
        self.qmxj = qmxj

    def add(self):
        db.session.add(self)

