# coding:utf-8
from flask import Module, session, request, render_template, redirect, url_for,flash

from scapp import db
from scapp.config import logger

from scapp.models.credit_data.sc_balance_sheet import SC_Balance_Sheet

from scapp import app

# 贷款调查——微贷(资产负债表)
@app.route('/Process/dqdc/dqdcXed_zcfzb/<int:loan_apply_id>', methods=['GET','POST'])
def dqdcXed_zcfzb(loan_apply_id):
	if request.method == 'GET':
		balance_sheets = SC_Balance_Sheet.query.filter_by(loan_apply_id=loan_apply_id).order_by("id").all()
		count_0 = SC_Balance_Sheet.query.filter_by(loan_apply_id=loan_apply_id,loan_type=0).count()
		count_2 = SC_Balance_Sheet.query.filter_by(loan_apply_id=loan_apply_id,loan_type=2).count()
		count_4 = SC_Balance_Sheet.query.filter_by(loan_apply_id=loan_apply_id,loan_type=4).count()
		count_6 = SC_Balance_Sheet.query.filter_by(loan_apply_id=loan_apply_id,loan_type=6).count()
		count_10 = SC_Balance_Sheet.query.filter_by(loan_apply_id=loan_apply_id,loan_type=10).count()
		count_12 = SC_Balance_Sheet.query.filter_by(loan_apply_id=loan_apply_id,loan_type=12).count()
		return render_template("Process/dqdc/dqdcXed_zcfzb.html",loan_apply_id=loan_apply_id,
			balance_sheets=balance_sheets,count_0=count_0,count_2=count_2,count_4=count_4,count_6=count_6,
			count_10=count_10,count_12=count_12)
	else:
		try:
			SC_Balance_Sheet.query.filter_by(loan_apply_id=loan_apply_id).delete()
			db.session.flush()

			for i in range(34):
				for j in range(len(request.form.getlist('type_%s' % i))):
					SC_Balance_Sheet(loan_apply_id,i,request.form.getlist('name_%s' % i)[j],
						j,request.form.getlist('value_%s' % i)[j]).add()

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