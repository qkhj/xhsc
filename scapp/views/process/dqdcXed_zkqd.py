# coding:utf-8
from flask import Module, session, request, render_template, redirect, url_for,flash

from scapp import db
from scapp.config import logger

from scapp.models.credit_data.sc_accounts_list import SC_Accounts_List

from scapp import app
from scapp.logic.total import Examine

# 贷款调查——小额贷款(账款清单)
@app.route('/Process/dqdc/dqdcXed_zkqd/<int:id>', methods=['GET'])
def dqdcXed_zkqd(id):
	accounts_list = SC_Accounts_List.query.filter_by(loan_apply_id=id).all()
	return render_template("Process/dqdc/dqdcXed_zkqd.html",id=id,accounts_list=accounts_list)

# 贷款调查——新增小额贷款(账款清单)
@app.route('/Process/dqdc/new_zkqd', methods=['GET','POST'])
def new_zkqd():
	loan_apply_id = request.form["hiddenId"]
	examine = Examine()
	#先删除所有记录
	examine.deleteList(loan_apply_id)
	#新增
	examine.addList(loan_apply_id,request)
	return redirect('Process/dqdc/dqdcXed_zkqd/' + loan_apply_id)

# 贷款调查——编辑小额贷款(账款清单)
@app.route('/Process/dqdc/edit_zkqd/<int:id>', methods=['GET','POST'])
def edit_zkqd(id):
	if request.method == 'GET':
		accounts_list = SC_Accounts_List.query.filter_by(id=id).first()
		return render_template("Process/dqdc/edit_zkqd.html",accounts_list=accounts_list)
	else:
		try:
			accounts_list = SC_Accounts_List.query.filter_by(id=id).first()
			accounts_list.name = request.form['name']
			accounts_list.original_price = request.form['original_price']
			accounts_list.occur_date = request.form['occur_date']
			accounts_list.deadline = request.form['deadline']
			accounts_list.present_price = request.form['present_price']
			accounts_list.cooperation_history = request.form['cooperation_history']
			accounts_list.average_period = request.form['average_period']
			accounts_list.trading_frequency = request.form['trading_frequency']
			accounts_list.turnover = request.form['turnover']
			accounts_list.pay_type = request.form['pay_type']
			accounts_list.source = request.form['source']
			accounts_list.other_info = request.form['other_info']

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