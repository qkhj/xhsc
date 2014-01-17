# coding:utf-8

import os

from flask import Module, session, request, render_template, redirect, url_for,flash
from flask.ext.login import current_user
import datetime

from scapp import db
from scapp.config import logger
from scapp.config import PER_PAGE

from scapp.models.credit_data.sc_cash_flow import SC_Cash_Flow
from scapp.models.credit_data.sc_cash_flow_assist import SC_Cash_Flow_Assist

from scapp import app

# 贷款调查——小额贷款(现金流分析)
@app.route('/Process/dqdc/dqdcXed_xjlfx/<int:id>', methods=['GET'])
def dqdcXed_xjlfx(id):
	cash_flow = SC_Cash_Flow.query.filter_by(loan_apply_id=id,type=1).all()
	cash_flow_assist_0 = SC_Cash_Flow_Assist.query.filter_by(loan_apply_id=id,type=1,assist_type=0).all()
	cash_flow_assist_1 = SC_Cash_Flow_Assist.query.filter_by(loan_apply_id=id,type=1,assist_type=1).all()
	cash_flow_assist_2 = SC_Cash_Flow_Assist.query.filter_by(loan_apply_id=id,type=1,assist_type=2).all()
	cash_flow_assist_3 = SC_Cash_Flow_Assist.query.filter_by(loan_apply_id=id,type=1,assist_type=3).all()
	if len(cash_flow) == 0: #用空串初始化cash_flow
		cash_flow = [0 for i in range(13)]
		cash_flow = ['']*13

	return render_template("Process/dqdc/dqdcXed_xjlfx.html",id=id,cash_flow=cash_flow,
		cash_flow_assist_0=cash_flow_assist_0,cash_flow_assist_1=cash_flow_assist_1,
		cash_flow_assist_2=cash_flow_assist_2,cash_flow_assist_3=cash_flow_assist_3)

# 贷款调查——编辑小额贷款(现金流分析)
@app.route('/Process/dqdc/edit_dqdcXed_xjlfx/<int:id>', methods=['POST'])
def edit_dqdcXed_xjlfx(id):
	try:
		#保存现金流
		cash_flow = SC_Cash_Flow.query.filter_by(loan_apply_id=id,type=1).order_by("id").all()

		early_cash_list = request.form.getlist('early_cash')
		sale_amount_list = request.form.getlist('sale_amount')
		accounts_receivable_list = request.form.getlist('accounts_receivable')
		prepaments_list = request.form.getlist('prepaments')
		total_cash_flow_list = request.form.getlist('total_cash_flow')
		cash_purchase_list = request.form.getlist('cash_purchase')
		accounts_payable_list = request.form.getlist('accounts_payable')
		advance_purchases_list = request.form.getlist('advance_purchases')
		total_cash_outflow_list = request.form.getlist('total_cash_outflow')
		wage_labor_list = request.form.getlist('wage_labor')
		tax_list = request.form.getlist('tax')
		transportation_costs_list = request.form.getlist('transportation_costs')
		rent_list = request.form.getlist('rent')
		maintenance_fees_list = request.form.getlist('maintenance_fees')
		utility_bills_list = request.form.getlist('utility_bills')
		advertising_fees_list = request.form.getlist('advertising_fees')
		social_intercourse_fees_list = request.form.getlist('social_intercourse_fees')
		fixed_costs_list = request.form.getlist('fixed_costs')
		fixed_asset_investment_list = request.form.getlist('fixed_asset_investment')
		disposal_of_fixed_assets_list = request.form.getlist('disposal_of_fixed_assets')
		investment_cash_flow_list = request.form.getlist('investment_cash_flow')
		bank_loans_list = request.form.getlist('bank_loans')
		repayments_bank_list = request.form.getlist('repayments_bank')
		financing_cash_flow_list = request.form.getlist('financing_cash_flow')
		household_expenditure_list = request.form.getlist('household_expenditure')
		private_use_list = request.form.getlist('private_use')
		private_cash_flow_list = request.form.getlist('private_cash_flow')
		ljxj_list = request.form.getlist('ljxj')
		qmxj_list = request.form.getlist('qmxj')

		if len(cash_flow) == 0: 
			# 循环获取表单
			for i in range(len(early_cash_list)):
				SC_Cash_Flow(id,1,i,
		    		early_cash_list[i],sale_amount_list[i],
					accounts_receivable_list[i],prepaments_list[i],
		            total_cash_flow_list[i],cash_purchase_list[i],
		            accounts_payable_list[i],advance_purchases_list[i],
		            total_cash_outflow_list[i],wage_labor_list[i],
		            tax_list[i],transportation_costs_list[i],
		            rent_list[i],maintenance_fees_list[i],
		            utility_bills_list[i],advertising_fees_list[i],
		            social_intercourse_fees_list[i],fixed_costs_list[i],
		            fixed_asset_investment_list[i],disposal_of_fixed_assets_list[i],
		            investment_cash_flow_list[i],
		            bank_loans_list[i],repayments_bank_list[i],
		            financing_cash_flow_list[i],household_expenditure_list[i],
		            private_use_list[i],private_cash_flow_list[i],
		            ljxj_list[i],qmxj_list[i]).add()
		else:
			for i in range(0, 13):
				SC_Cash_Flow.query.filter_by(loan_apply_id=id,type=1,month=i).update({
		    		"early_cash":early_cash_list[i],"sale_amount":sale_amount_list[i],
					"accounts_receivable":accounts_receivable_list[i],"prepaments":prepaments_list[i],
		            "total_cash_flow":total_cash_flow_list[i],"cash_purchase":cash_purchase_list[i],
		            "accounts_payable":accounts_payable_list[i],"advance_purchases":advance_purchases_list[i],
		            "total_cash_outflow":total_cash_outflow_list[i],"wage_labor":wage_labor_list[i],
		            "tax":tax_list[i],"transportation_costs":transportation_costs_list[i],
		            "rent":rent_list[i],"maintenance_fees":maintenance_fees_list[i],
		            "utility_bills":utility_bills_list[i],"advertising_fees":advertising_fees_list[i],
		            "social_intercourse_fees":social_intercourse_fees_list[i],"fixed_costs":fixed_costs_list[i],
		            "fixed_asset_investment":fixed_asset_investment_list[i],"disposal_of_fixed_assets":disposal_of_fixed_assets_list[i],
		            "investment_cash_flow":investment_cash_flow_list[i],
		            "bank_loans":bank_loans_list[i],"repayments_bank":repayments_bank_list[i],
		            "financing_cash_flow":financing_cash_flow_list[i],"household_expenditure":household_expenditure_list[i],
		            "private_use":private_use_list[i],"private_cash_flow":private_cash_flow_list[i],
		            "ljxj":ljxj_list[i],"qmxj":qmxj_list[i]})

		#保存现金流其他信息
		name_cash_flow_assist_0_list = request.form.getlist('name_cash_flow_assist_0')
		name_cash_flow_assist_1_list = request.form.getlist('name_cash_flow_assist_1')
		name_cash_flow_assist_2_list = request.form.getlist('name_cash_flow_assist_2')
		name_cash_flow_assist_3_list = request.form.getlist('name_cash_flow_assist_3')
		len0 = len(name_cash_flow_assist_0_list)
		len1 = len(name_cash_flow_assist_1_list)
		len2 = len(name_cash_flow_assist_2_list)
		len3 = len(name_cash_flow_assist_3_list)

		month_0_list = request.form.getlist('month_0')
		month_1_list = request.form.getlist('month_1')
		month_2_list = request.form.getlist('month_2')
		month_3_list = request.form.getlist('month_3')
		month_4_list = request.form.getlist('month_4')
		month_5_list = request.form.getlist('month_5')
		month_6_list = request.form.getlist('month_6')
		month_7_list = request.form.getlist('month_7')
		month_8_list = request.form.getlist('month_8')
		month_9_list = request.form.getlist('month_9')
		month_10_list = request.form.getlist('month_10')
		month_11_list = request.form.getlist('month_11')
		month_12_list = request.form.getlist('month_12')

		SC_Cash_Flow_Assist.query.filter_by(loan_apply_id=id,type=1,assist_type=0).delete()
		db.session.flush()
		for i in range(0,len0):
			SC_Cash_Flow_Assist(id,1,0,name_cash_flow_assist_0_list[i],month_0_list[i],
		    	month_1_list[i],month_2_list[i],month_3_list[i],month_4_list[i],month_5_list[i],
		    	month_6_list[i],month_7_list[i],month_8_list[i],month_9_list[i],month_10_list[i],
		        month_11_list[i],month_12_list[i]).add()

		SC_Cash_Flow_Assist.query.filter_by(loan_apply_id=id,type=1,assist_type=1).delete()
		db.session.flush()
		for i in range(len0,len0+len1):
			SC_Cash_Flow_Assist(id,1,1,name_cash_flow_assist_1_list[i-len0],month_0_list[i],
		    	month_1_list[i],month_2_list[i],month_3_list[i],month_4_list[i],month_5_list[i],
		    	month_6_list[i],month_7_list[i],month_8_list[i],month_9_list[i],month_10_list[i],
		        month_11_list[i],month_12_list[i]).add()

		SC_Cash_Flow_Assist.query.filter_by(loan_apply_id=id,type=1,assist_type=2).delete()
		db.session.flush()
		for i in range(len0+len1,len0+len1+len2):
			SC_Cash_Flow_Assist(id,1,2,name_cash_flow_assist_2_list[i-len0-len1],month_0_list[i],
		    	month_1_list[i],month_2_list[i],month_3_list[i],month_4_list[i],month_5_list[i],
		    	month_6_list[i],month_7_list[i],month_8_list[i],month_9_list[i],month_10_list[i],
		        month_11_list[i],month_12_list[i]).add()

		SC_Cash_Flow_Assist.query.filter_by(loan_apply_id=id,type=1,assist_type=3).delete()
		db.session.flush()
		for i in range(len0+len1+len2,len0+len1+len2+len3):
			print i-len0-len1-len2
			SC_Cash_Flow_Assist(id,1,3,name_cash_flow_assist_3_list[i-len0-len1-len2],month_0_list[i],
		    	month_1_list[i],month_2_list[i],month_3_list[i],month_4_list[i],month_5_list[i],
		    	month_6_list[i],month_7_list[i],month_8_list[i],month_9_list[i],month_10_list[i],
		        month_11_list[i],month_12_list[i]).add()

		# 事务提交
		db.session.commit()
		# 消息闪现
		flash('保存成功','success')
	except:
		# 回滚
		db.session.rollback()
		logger.exception('exception')
		# 消息闪现
		flash('保存失败','error')

	return redirect('Process/dqdc/dqdc')
    