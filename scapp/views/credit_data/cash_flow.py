#coding:utf-8
__author__ = 'Johnny'
from scapp import db,app
from scapp.config import logger
from flask import request
import json
from json import encoder
from scapp.models.credit_data import sc_cash_flow
# 新增现金流
@app.route('/Process/dqdc/new_xjlfx', methods=['GET','POST'])
def new_xjlfx(id,type,loan_apply_id):
    if request.method == 'POST':
        result={'result':'success'}
        try:
            cash_flow( request.form['loan_apply_id'],request.form['type'],request.form['month'],request.form['early_cash'],
                        request.form['sale_amount'],request.form['accounts_receivable'],request.form['prepaments'],
                        request.form['total_cash_flow'],request.form['cash_purchase'],request.form['accounts_payable'],
                        request.form['advance_purchases'],request.form['total_cash_outflow'],
                        request.form['wage_labor'],request.form['tax'],
                        request.form['transportation_costs'],request.form['rent'],request.form['maintenance_fees'],
                        request.form['utility_bills'],request.form['advertising_fees'],request.form['social_intercourse_fees'],
                        request.form['fixed_asset_investment'],request.form['disposal_of_fixed_assets'],
                        request.form['investment_cash_flow'],request.form['bank_loans'],request.form['repayments_bank'],
                        request.form['financing_cash_flow'],request.form['household_expenditure'],request.form['private_use'],
                        request.form['private_cash_flow'],request.form['fixed_costs'],
            ).add()
            # 事务提交
            db.session.commit()
            # 消息闪现
            #flash('保存成功','Success')
        except:
            # 回滚
            db.session.rollback()
            logger.exception('exception')
            # 消息闪现
            #flash('保存失败','Error')
            result={'result':'fail'}
        finally:
            return json.dumps(result,ensure_ascii=False)
    else :
        cash_flow_data = cash_flow.query.filter_by(loan_apply_id==loan_apply_id,type==type).first()
        encoder.FLOAT_REPR = lambda o: format(o, '.2f')#使float类型字段只显示两位小数
        return json.dumps(cash_flow_data,ensure_ascii=False)