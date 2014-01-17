# coding:utf-8
from flask import Module, session, request, render_template, redirect, url_for,flash

from scapp import db
from scapp.config import logger

from scapp.models.credit_data.sc_stock import SC_Stock

from scapp import app

# 贷款调查——小额贷款(库存)
@app.route('/Process/dqdc/dqdcXed_kc/<int:id>', methods=['GET'])
def dqdcXed_kc(id):
	stock = SC_Stock.query.filter_by(loan_apply_id=id).all()
	return render_template("Process/dqdc/dqdcXed_kc.html",id=id,stock=stock)

# 贷款调查——新增小额贷款(库存)
@app.route('/Process/dqdc/new_kc/<int:loan_apply_id>', methods=['GET','POST'])
def new_kc(loan_apply_id):
	if request.method == 'GET':
		return render_template("Process/dqdc/new_kc.html",loan_apply_id=loan_apply_id)
	else:
		try:
			SC_Stock(loan_apply_id,request.form['name'],request.form['amount'],
				request.form['purchase_price'],request.form['purchase_total_price'],
				request.form['sell_price'],request.form['sell_total_price'],
				request.form['pre_rate']).add()

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

# 贷款调查——编辑小额贷款(库存)
@app.route('/Process/dqdc/edit_kc/<int:id>', methods=['GET','POST'])
def edit_kc(id):
	if request.method == 'GET':
		stock = SC_Stock.query.filter_by(id=id).first()
		return render_template("Process/dqdc/edit_kc.html",stock=stock)
	else:
		try:
			stock = SC_Stock.query.filter_by(id=id).first()
			stock.name = request.form['name']
			stock.amount = request.form['amount']
			stock.purchase_price = request.form['purchase_price']
			stock.purchase_total_price = request.form['purchase_total_price']
			stock.sell_price = request.form['sell_price']
			stock.sell_total_price = request.form['sell_total_price']
			stock.pre_rate = request.form['pre_rate']

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