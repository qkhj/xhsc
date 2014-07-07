# coding:utf-8
from flask import Module, session, request, render_template, redirect, url_for,flash

from scapp import db
from scapp.config import logger

from scapp.models.credit_data.sc_stock import SC_Stock

from scapp import app

# 贷款调查——小额贷款(库存)
@app.route('/Process/dqdc/dqdcXed_kc/<int:loan_apply_id>', methods=['GET'])
def dqdcXed_kc(loan_apply_id):
	stocks = SC_Stock.query.filter_by(loan_apply_id=loan_apply_id).all()
	return render_template("Process/dqdc/dqdcXed_kc.html",loan_apply_id=loan_apply_id,stocks=stocks)

# 贷款调查——新增小额贷款(库存)
@app.route('/Process/dqdc/new_kc/<int:loan_apply_id>', methods=['POST'])
def new_kc(loan_apply_id):
	try:
		SC_Stock.query.filter_by(loan_apply_id=loan_apply_id).delete()
		db.session.flush()

		name_list = request.form.getlist('name')
		amount_list = request.form.getlist('amount')
		purchase_price_list = request.form.getlist('purchase_price')
		purchase_total_price_list = request.form.getlist('purchase_total_price')

		# 循环获取表单
		for i in range(len(name_list)):
			SC_Stock(loan_apply_id,name_list[i],amount_list[i],
				purchase_price_list[i],purchase_total_price_list[i],None,None,None).add()

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
			
	return redirect('Process/dqdc/dqdcXed_kc/%d' % loan_apply_id)


# 打印库存
@app.route('/Process/dqdc/dy_dhd/<int:loan_apply_id>', methods=['GET'])
def dy_dhd(loan_apply_id):
	stocks = SC_Stock.query.filter_by(loan_apply_id=loan_apply_id).all()
	return render_template("Print/dy_dhd.html",loan_apply_id=loan_apply_id,stocks=stocks)