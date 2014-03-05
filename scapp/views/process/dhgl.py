# coding:utf-8

import os

from flask import Module, session, request, render_template, redirect, url_for,flash
from flask.ext.login import current_user
import datetime

from scapp import db
from scapp.config import logger
from scapp.config import PER_PAGE
from scapp.config import PROCESS_STATUS_SPJY_TG
from scapp.config import PROCESS_STATUS_DKFKJH
from scapp.models import SC_Monitor
from scapp.models import SC_Balance_Sheet_Fbz
from scapp.models import SC_Profit_Loss_Fbz
from scapp.models import View_Query_Loan
from scapp.logic.total import Total
from scapp.logic.total import User
from scapp import app
from scapp.pojo.bz_check_form import CheckForm

# 贷后管理
@app.route('/Process/dhgl/dhgl', methods=['GET'])
def Process_dhgl():
    return render_template("Process/dhgl/dhgl_search.html")

# 贷后管理搜索
@app.route('/Process/dhgl/dhgl_search/<int:page>', methods=['GET','POST'])
def dhgl_search(page):
	customer_name = request.form['customer_name']
	loan_type = request.form['loan_type']
	sql = ""
	if loan_type != '0':
	    sql = "loan_type='"+loan_type+"' and "
	sql += " process_status='"+PROCESS_STATUS_DKFKJH+"'"
	sql += " and (A_loan_officer="+str(current_user.id)+" or B_loan_officer="+str(current_user.id)+" or yunying_loan_officer="+str(current_user.id)+")"

	if customer_name:
	    sql += " and (company_customer_name like '%"+customer_name+"%' or individual_customer_name like '%"+customer_name+"%')"

	loan_apply = View_Query_Loan.query.filter(sql).paginate(page, per_page = PER_PAGE)
	return render_template("Process/dhgl/dhgl.html",loan_apply=loan_apply,customer_name=customer_name,loan_type=loan_type)

# 贷后管理——新增标准
@app.route('/Process/dhgl/new_bz/<int:loan_apply_id>', methods=['GET'])
def new_bz(loan_apply_id):
	loan_apply = View_Query_Loan.query.filter_by(loan_apply_id=loan_apply_id).first()

	checkForm = getCheckForm(loan_apply_id,loan_apply)
	monitorList = SC_Monitor.query.filter_by(loan_apply_id=loan_apply_id).all()
	return render_template("Process/dhgl/new_bz.html",loan_apply=loan_apply,monitorList=monitorList,loan_apply_id=loan_apply_id,checkForm=checkForm)

# 贷后管理——保存新标准
@app.route('/Process/dhgl/new_bz_save', methods=['POST'])
def new_bz_save():
	total = Total()
	loan_apply_id = request.form["hiddenId"]
	#先删除所有标准
	total.deleteBZ(loan_apply_id)	
	#新增页面所有标准
	total.addNewBZ(loan_apply_id,request)
	loan_apply = View_Query_Loan.query.filter_by(loan_apply_id=loan_apply_id).first()
	monitorList = SC_Monitor.query.filter_by(loan_apply_id=loan_apply_id).all()
	checkForm = getCheckForm(loan_apply_id,loan_apply)
	return render_template("Process/dhgl/new_bz.html",loan_apply=loan_apply,monitorList=monitorList,checkForm=checkForm)

#获取前台form表单
def getCheckForm(loan_apply_id,loan_apply):
	#前台form表单
	checkForm = CheckForm()
	#借款人#客户号
	if loan_apply.individual_customer_name:
		checkForm.jkr = loan_apply.individual_customer_name
		checkForm.khId = loan_apply.individual_customer_id
	if loan_apply.company_customer_name:
		checkForm.jkr = loan_apply.company_customer_name
		checkForm.khId = loan_apply.company_customer_id
	#客户经理
	A_loan = loan_apply.A_loan_officer
	B_loan = loan_apply.B_loan_officer
	yunying_loan = loan_apply.yunying_loan_officer
	user = User()
	A_name = user.getUserName(A_loan)
	B_name = user.getUserName(B_loan)
	yunying_name = user.getUserName(yunying_loan)
	checkForm.khjl= A_name + ","+ B_name + "," + yunying_name
	#合同号
	pactInform = Total().getInformByloadId(loan_apply_id)
	checkForm.hkId = pactInform.loan_contract_number
	#贷款金额
	checkForm.dkje = pactInform.amount
	#放款日
	checkForm.fkDate = pactInform.loan_date
	#到期日
	checkForm.dqDate = pactInform.last_repayment_date
	#利率
	checkForm.lv = pactInform.rates
	#期数
	checkForm.hkqs = pactInform.deadline
	return checkForm

# 贷后管理——非标准
@app.route('/Process/dhgl/fbz/<int:loan_apply_id>', methods=['GET'])
def fbz(loan_apply_id):
	fbz = SC_Balance_Sheet_Fbz.query.filter_by(loan_apply_id=loan_apply_id).all()
	return render_template("Process/dhgl/fbz.html",loan_apply_id=loan_apply_id,fbz=fbz)

# 贷后管理——新增非标准
@app.route('/Process/dhgl/new_fbz/<int:loan_apply_id>', methods=['GET','POST'])
def new_fbz(loan_apply_id):
	if request.method == 'GET':
		return render_template("Process/dhgl/new_fbz.html",loan_apply_id=loan_apply_id)
	else:
		try:
			index = SC_Balance_Sheet_Fbz.query.filter_by(loan_apply_id=loan_apply_id).count()
		    # 保存资产负债表
			SC_Balance_Sheet_Fbz(loan_apply_id,index, request.form['cash_deposit'],request.form['payable'],
				request.form['receivable'],request.form['short_loan'],request.form['stock'],request.form['long_loan'],
				request.form['total_current_assets'],request.form['total_debt'],request.form['total_fixed_assets'],
				request.form['owner_equity'],request.form['total_assets'],request.form['debt_and_owner_equity'],
				request.form['remark']).add()
		    
		    # 保存损益表
			SC_Profit_Loss_Fbz(loan_apply_id, index,request.form['income'],request.form['cost'],
				request.form['gross_profit'],request.form['salary'],request.form['insurance'],request.form['rent'],
				request.form['freight'],request.form['maintain'],request.form['utility'],request.form['stock_loss'],
				request.form['taxes'],request.form['others'],request.form['stages'],request.form['total_cost'],
				request.form['net_profit'],request.form['other_pay'],request.form['other_income'],
				request.form['family_income'],request.form['remark1'],request.form['remark2']).add()

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
		
		return redirect('Process/dhgl/fbz/%d' % loan_apply_id) 
    
# 贷后管理——非标准
@app.route('/Process/dhgl/edit_fbz/<int:loan_apply_id>/<int:index>', methods=['GET','POST'])
def edit_fbz(loan_apply_id,index):
	if request.method == 'GET':
		balance_sheet_fbz = SC_Balance_Sheet_Fbz.query.filter_by(loan_apply_id=loan_apply_id,index=index).first()
		profit_loss_fbz = SC_Profit_Loss_Fbz.query.filter_by(loan_apply_id=loan_apply_id,index=index).first()
		return render_template("Process/dhgl/edit_fbz.html",loan_apply_id=loan_apply_id,index=index,
			balance_sheet_fbz=balance_sheet_fbz,profit_loss_fbz=profit_loss_fbz)
	else:
		try:
			# 保存资产负债表
			balance_sheet_fbz = SC_Balance_Sheet_Fbz.query.filter_by(loan_apply_id=loan_apply_id,index=index).first()
			balance_sheet_fbz.cash_deposit = request.form['cash_deposit']
			balance_sheet_fbz.payable = request.form['payable']
			balance_sheet_fbz.receivable = request.form['receivable']
			balance_sheet_fbz.short_loan = request.form['short_loan']
			balance_sheet_fbz.stock = request.form['stock']
			balance_sheet_fbz.long_loan = request.form['long_loan']
			balance_sheet_fbz.total_current_assets = request.form['total_current_assets']
			balance_sheet_fbz.total_debt = request.form['total_debt']
			balance_sheet_fbz.total_fixed_assets = request.form['total_fixed_assets']
			balance_sheet_fbz.owner_equity = request.form['owner_equity']
			balance_sheet_fbz.total_assets = request.form['total_assets']
			balance_sheet_fbz.debt_and_owner_equity = request.form['debt_and_owner_equity']
			balance_sheet_fbz.remark = request.form['remark']

			# 保存损益表
			profit_loss_fbz = SC_Profit_Loss_Fbz.query.filter_by(loan_apply_id=loan_apply_id,index=index).first()
			profit_loss_fbz.income = request.form['income']
			profit_loss_fbz.cost = request.form['cost']
			profit_loss_fbz.gross_profit = request.form['gross_profit']
			profit_loss_fbz.salary = request.form['salary']
			profit_loss_fbz.insurance = request.form['insurance']
			profit_loss_fbz.rent = request.form['rent']
			profit_loss_fbz.freight = request.form['freight']
			profit_loss_fbz.maintain = request.form['maintain']
			profit_loss_fbz.utility = request.form['utility']
			profit_loss_fbz.stock_loss = request.form['stock_loss']
			profit_loss_fbz.taxes = request.form['taxes']
			profit_loss_fbz.others = request.form['others']
			profit_loss_fbz.stages = request.form['stages']
			profit_loss_fbz.total_cost = request.form['total_cost']
			profit_loss_fbz.net_profit = request.form['net_profit']
			profit_loss_fbz.other_pay = request.form['other_pay']
			profit_loss_fbz.other_income = request.form['other_income']
			profit_loss_fbz.family_income = request.form['family_income']
			profit_loss_fbz.remark1 = request.form['remark1']
			profit_loss_fbz.remark2 = request.form['remark2']

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
		
		return redirect('Process/dhgl/fbz/%d' % loan_apply_id) 

# 贷后管理——管理信息列表
@app.route('/Process/dhgl/glxxlb', methods=['GET'])
def dhgl_glxxlb():
    return render_template("Process/dhgl/glxxlb.html")

# 贷后管理——管理信息
@app.route('/Process/dhgl/glxx', methods=['GET'])
def dhgl_glxx():
    return render_template("Process/dhgl/glxx.html")

# 贷后管理——非标监控说明
@app.route('/Process/dhgl/fbjksm', methods=['GET'])
def dhgl_fbjksm():
    return render_template("Process/dhgl/fbjksm.html")