# coding:utf-8
from flask import Module, session, request, render_template, redirect, url_for,flash

from scapp import db
from scapp.config import logger

from scapp.models.credit_data.sc_cross_examination import SC_Cross_Examination

from scapp import app

# 贷款调查——小额贷款(交叉检验)
@app.route('/Process/dqdc/dqdcXed_jcjy/<int:id>', methods=['GET'])
def dqdcXed_jcjy(id):
	cross_examination = SC_Cross_Examination.query.filter_by(loan_apply_id=id).first()
	return render_template("Process/dqdc/dqdcXed_jcjy.html",id=id,cross_examination=cross_examination)

# 贷款调查——编辑小额贷款(交叉检验)
@app.route('/Process/dqdc/edit_dqdcXed_jcjy/<int:id>', methods=['POST'])
def edit_dqdcXed_jcjy(id):
	try:
		cross_examination = SC_Cross_Examination.query.filter_by(loan_apply_id=id).first()
		if cross_examination:
			cross_examination.initial_equity = request.form['initial_equity']
			cross_examination.profit_period = request.form['profit_period']
			cross_examination.injection_period = request.form['injection_period']
			cross_examination.pick_period = request.form['pick_period']
			cross_examination.depreciation = request.form['depreciation']
			cross_examination.appreciation = request.form['appreciation']
			cross_examination.due_rights = request.form['due_rights']
			cross_examination.fact_rights = request.form['fact_rights']
			cross_examination.dif_rate = request.form['dif_rate']
			cross_examination.right_explanation = request.form['right_explanation']
			cross_examination.business_cross = request.form['business_cross']
			cross_examination.cost_structure = request.form['cost_structure']
			cross_examination.risk_analysis = request.form['risk_analysis']
		else:
			SC_Cross_Examination(id,request.form['initial_equity'],
				request.form['profit_period'],request.form['injection_period'],
				request.form['pick_period'],request.form['depreciation'],
				request.form['appreciation'],request.form['due_rights'],
				request.form['fact_rights'],request.form['dif_rate'],
				request.form['right_explanation'],request.form['business_cross'],
				request.form['cost_structure'],request.form['risk_analysis']).add()

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