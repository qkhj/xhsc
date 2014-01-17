# coding:utf-8
from flask import Module, session, request, render_template, redirect, url_for,flash

from scapp import db
from scapp.config import logger

from scapp.models.credit_data.sc_assets_deposit import SC_Assets_Deposit
from scapp.models.credit_data.sc_assets_acceptances import SC_Assets_Acceptances
from scapp.models.credit_data.sc_assets_receivable import SC_Assets_Receivable
from scapp.models.credit_data.sc_assets_stock import SC_Assets_Stock
from scapp.models.credit_data.sc_assets_fixed_assets import SC_Assets_Fixed_Assets
from scapp.models.credit_data.sc_assets_other_operate_assets import SC_Assets_Other_Operate_Assets
from scapp.models.credit_data.sc_assets_other_non_operate import SC_Assets_Other_Non_Operate

from scapp import app

# 贷款调查——小额贷款(资产负债表)
@app.route('/Process/dqdc/dqdcXed_zcfzb/<belong_customer_type>/<int:belong_customer_value>/<int:id>', methods=['GET'])
def dqdcXed_zcfzb(belong_customer_type,belong_customer_value,id):
	assets_deposit = SC_Assets_Deposit.query.filter_by(loan_apply_id=id).all()
	assets_acceptances = SC_Assets_Acceptances.query.filter_by(loan_apply_id=id).all()
	assets_receivable_0 = SC_Assets_Receivable.query.filter_by(loan_apply_id=id,accounts_type=0).all()
	assets_receivable_1 = SC_Assets_Receivable.query.filter_by(loan_apply_id=id,accounts_type=1).all()
	assets_stock = SC_Assets_Stock.query.filter_by(loan_apply_id=id).all()
	assets_fixed_assets_0 = SC_Assets_Fixed_Assets.query.filter_by(loan_apply_id=id,assets_type=0).all()
	assets_fixed_assets_1 = SC_Assets_Fixed_Assets.query.filter_by(loan_apply_id=id,assets_type=1).all()
	assets_fixed_assets_2 = SC_Assets_Fixed_Assets.query.filter_by(loan_apply_id=id,assets_type=2).all()
	assets_other_operate_assets = SC_Assets_Other_Operate_Assets.query.filter_by(loan_apply_id=id).all()
	assets_other_non_operate = SC_Assets_Other_Non_Operate.query.filter_by(loan_apply_id=id).all()

	return render_template("Process/dqdc/dqdcXed_zcfzb.html",id=id,assets_deposit=assets_deposit,
		assets_acceptances=assets_acceptances,assets_receivable_0=assets_receivable_0,
		assets_receivable_1=assets_receivable_1,
		assets_stock=assets_stock,
		assets_fixed_assets_0=assets_fixed_assets_0,assets_fixed_assets_1=assets_fixed_assets_1,
		assets_fixed_assets_2=assets_fixed_assets_2,
		assets_other_operate_assets=assets_other_operate_assets,
		assets_other_non_operate=assets_other_non_operate)

# 贷款调查——编辑小额贷款(总资产)
@app.route('/Process/dqdc/edit_zzc/<int:loan_apply_id>', methods=['POST'])
def edit_zzc(loan_apply_id):
	try:
		#资产负债表-存款
		SC_Assets_Deposit.query.filter_by(loan_apply_id=loan_apply_id).delete()
		db.session.flush()

		bank_ad_list = request.form.getlist('bank_ad')
		account_type_ad_list = request.form.getlist('account_type_ad')
		account_no_ad_list = request.form.getlist('account_no_ad')
		account_balance_ad_list = request.form.getlist('account_balance_ad')
		# 循环获取表单
		for i in range(len(bank_ad_list)):
			SC_Assets_Deposit(loan_apply_id,bank_ad_list[i],account_type_ad_list[i],
		    	account_no_ad_list[i],account_balance_ad_list[i]).add()

		#资产负债表-承兑汇票
		SC_Assets_Acceptances.query.filter_by(loan_apply_id=id).delete()
		db.session.flush()

		bank_ac_list = request.form.getlist('bank_ac')
		account_expiry_date_ac_list = request.form.getlist('account_expiry_date_ac')
		account_balance_ac_list = request.form.getlist('account_balance_ac')
		# 循环获取表单
		for i in range(len(bank_ad_list)):
		    SC_Assets_Acceptances(loan_apply_id,bank_ac_list[i],account_expiry_date_ac_list[i],
		        account_balance_ac_list[i]).add()

		#资产负债表-应收账款,预付账款
		SC_Assets_Receivable.query.filter_by(loan_apply_id=id,accounts_type=0).delete()
		db.session.flush()

		customer_name_ar_0_list = request.form.getlist('customer_name_ar_0')
		describe_ar_0_list = request.form.getlist('describe_ar_0')
		proportion_ar_0_list = request.form.getlist('proportion_ar_0')
		amount_ar_0_list = request.form.getlist('amount_ar_0')
		# 循环获取表单
		for i in range(len(bank_ad_list)):
		    SC_Assets_Receivable(loan_apply_id,customer_name_ar_0_list[i],describe_ar_0_list[i],
		        proportion_ar_0_list[i],amount_ar_0_list[i]).add()

		#资产负债表-应收账款,预付账款
		SC_Assets_Receivable.query.filter_by(loan_apply_id=id,accounts_type=1).delete()
		db.session.flush()

		customer_name_ar_1_list = request.form.getlist('customer_name_ar_1')
		describe_ar_1_list = request.form.getlist('describe_ar_1')
		proportion_ar_1_list = request.form.getlist('proportion_ar_1')
		amount_ar_1_list = request.form.getlist('amount_ar_1')
		# 循环获取表单
		for i in range(len(bank_ad_list)):
		    SC_Assets_Receivable(loan_apply_id,customer_name_ar_1_list[i],describe_ar_1_list[i],
		        proportion_ar_1_list[i],amount_ar_1_list[i]).add()

		#资产负债表-存货
		SC_Assets_Stock.query.filter_by(loan_apply_id=id).delete()
		db.session.flush()

		stock_type_as_list = request.form.getlist('stock_type_as')
		stock_evaluate_as_list = request.form.getlist('stock_evaluate_as')
		stock_mobility_as_list = request.form.getlist('stock_mobility_as')
		proportion_as_list = request.form.getlist('proportion_as')
		amount_as_list = request.form.getlist('amount_as')

		# 循环获取表单
		for i in range(len(bank_ad_list)):
		    SC_Assets_Stock(loan_apply_id,stock_type_as_list[i],stock_evaluate_as_list[i],
		        stock_mobility_as_list[i],proportion_as_list[i],amount_as_list[i]).add()

		#资产分类 0:房地产 1:设备 2:车辆
		SC_Assets_Fixed_Assets.query.filter_by(loan_apply_id=id,assets_type=0).delete()
		db.session.flush()

		assets_name_afa_0_list = request.form.getlist('assets_name_afa_0')
		assets_ah_afa_0_list = request.form.getlist('assets_ah_afa_0')
		describe_afa_0_list = request.form.getlist('describe_afa_0')
		assets_date_afa_0_list = request.form.getlist('assets_date_afa_0')
		price_afa_0_list = request.form.getlist('price_afa_0')
		amount_afa_0_list = request.form.getlist('amount_afa_0')

		# 循环获取表单
		for i in range(len(bank_ad_list)):
		    SC_Assets_Fixed_Assets(loan_apply_id,assets_name_afa_0_list[i],assets_ah_afa_0_list[i],
		        describe_afa_0_list[i],assets_date_afa_0_list[i],price_afa_0_list[i],
		        amount_afa_0_list[i]).add()

		#资产分类 0:房地产 1:设备 2:车辆
		SC_Assets_Fixed_Assets.query.filter_by(loan_apply_id=id,assets_type=1).delete()
		db.session.flush()

		assets_name_afa_1_list = request.form.getlist('assets_name_afa_1')
		assets_ah_afa_1_list = request.form.getlist('assets_ah_afa_1')
		describe_afa_1_list = request.form.getlist('describe_afa_1')
		assets_date_afa_1_list = request.form.getlist('assets_date_afa_1')
		price_afa_1_list = request.form.getlist('price_afa_1')
		amount_afa_1_list = request.form.getlist('amount_afa_1')

		# 循环获取表单
		for i in range(len(bank_ad_list)):
		    SC_Assets_Fixed_Assets(loan_apply_id,assets_name_afa_1_list[i],assets_ah_afa_1_list[i],
		        describe_afa_1_list[i],assets_date_afa_1_list[i],price_afa_1_list[i],
		        amount_afa_1_list[i]).add()

		#资产分类 0:房地产 1:设备 2:车辆
		SC_Assets_Fixed_Assets.query.filter_by(loan_apply_id=id,assets_type=2).delete()
		db.session.flush()

		assets_name_afa_2_list = request.form.getlist('assets_name_afa_2')
		assets_ah_afa_2_list = request.form.getlist('assets_ah_afa_2')
		describe_afa_2_list = request.form.getlist('describe_afa_2')
		assets_date_afa_2_list = request.form.getlist('assets_date_afa_2')
		price_afa_2_list = request.form.getlist('price_afa_2')
		amount_afa_2_list = request.form.getlist('amount_afa_2')

		# 循环获取表单
		for i in range(len(bank_ad_list)):
		    SC_Assets_Fixed_Assets(loan_apply_id,assets_name_afa_2_list[i],assets_ah_afa_2_list[i],
		        describe_afa_2_list[i],assets_date_afa_2_list[i],price_afa_2_list[i],
		        amount_afa_2_list[i]).add()

		#资产负债表-其它经营资产
		SC_Assets_Other_Operate_Assets.query.filter_by(loan_apply_id=id).delete()
		db.session.flush()

		project_aooa_list = request.form.getlist('project_aooa')
		describe_aooa_list = request.form.getlist('describe_aooa')
		amount_aooa_list = request.form.getlist('amount_aooa')

		# 循环获取表单
		for i in range(len(bank_ad_list)):
		    SC_Assets_Other_Operate_Assets(loan_apply_id,project_aooa_list[i],describe_aooa_list[i],
		        amount_aooa_list[i]).add()

		#资产负债表-其它非经营资产
		SC_Assets_Other_Non_Operate.query.filter_by(loan_apply_id=id).delete()
		db.session.flush()

		project_aono_list = request.form.getlist('project_aono')
		project_owner_aono_list = request.form.getlist('project_owner_aono')
		describe_aono_list = request.form.getlist('describe_aono')
		amount_aono_list = request.form.getlist('amount_aono')

		# 循环获取表单
		for i in range(len(bank_ad_list)):
		    SC_Assets_Other_Non_Operate(loan_apply_id,project_aono_list[i],project_owner_aono_list[i],
		        describe_aono_list[i],amount_aono_list[i]).add()

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