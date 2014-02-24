# coding:utf-8
from flask import Module, session, request, render_template, redirect, url_for,flash

from scapp import db
from scapp.config import logger

from scapp.models.credit_data.sc_cross_examination import SC_Cross_Examination

from scapp import app

# 贷款调查——小额贷款(交叉检验)
@app.route('/Process/dqdc/dqdcXed_jcjy/<int:loan_apply_id>', methods=['GET','POST'])
def dqdcXed_jcjy(loan_apply_id):
	if request.method == 'GET':
		cross_examination = SC_Cross_Examination.query.filter_by(loan_apply_id=loan_apply_id).order_by("id").all()
		count_3 = SC_Cross_Examination.query.filter_by(loan_apply_id=loan_apply_id,loan_type=3).count()
		return render_template("Process/dqdc/dqdcXed_jcjy.html",loan_apply_id=loan_apply_id,
			cross_examination=cross_examination,count_3=count_3)
	else:
		try:
			SC_Cross_Examination.query.filter_by(loan_apply_id=loan_apply_id).delete()
			db.session.flush()

			for i in range(14):
				for j in range(len(request.form.getlist('type_%s' % i))):
					SC_Cross_Examination(loan_apply_id,i,request.form.getlist('name_%s' % i)[j],
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