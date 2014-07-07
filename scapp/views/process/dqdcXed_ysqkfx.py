# coding:utf-8
from flask import Module, session, request, render_template, redirect, url_for,flash

from scapp import db
from scapp.config import logger

from scapp.models.credit_data.sc_profit_loss import SC_Profit_Loss

from scapp import app

# 贷款调查——小额贷款(损益情况分析)
@app.route('/Process/dqdc/dqdcXed_ysqkfx/<int:loan_apply_id>', methods=['GET','POST'])
def dqdcXed_ysqkfx(loan_apply_id):
	if request.method == 'GET':
		profit_loss = SC_Profit_Loss.query.filter_by(loan_apply_id=loan_apply_id).order_by("id").all()
		count_1 = SC_Profit_Loss.query.filter_by(loan_apply_id=loan_apply_id,items_type=1).count()
		count_3 = SC_Profit_Loss.query.filter_by(loan_apply_id=loan_apply_id,items_type=3).count()
		count_21 = SC_Profit_Loss.query.filter_by(loan_apply_id=loan_apply_id,items_type=21).count()
		count_28 = SC_Profit_Loss.query.filter_by(loan_apply_id=loan_apply_id,items_type=28).count()
		count_29 = SC_Profit_Loss.query.filter_by(loan_apply_id=loan_apply_id,items_type=29).count()
		return render_template("Process/dqdc/dqdcXed_ysqkfx.html",loan_apply_id=loan_apply_id,profit_loss=profit_loss,
			count_1=count_1,count_3=count_3,count_21=count_21,count_28=count_28,count_29=count_29)
	else:
		try:
			SC_Profit_Loss.query.filter_by(loan_apply_id=loan_apply_id).delete()
			db.session.flush()

			for i in range(31):
				for j in range(len(request.form.getlist('items_name_%s' % i))):
					SC_Profit_Loss(loan_apply_id,i,request.form.getlist('items_name_%s' % i)[j],
						j,request.form.getlist('month_1_%s' % i)[j],request.form.getlist('month_2_%s' % i)[j],
						request.form.getlist('month_3_%s' % i)[j],request.form.getlist('month_4_%s' % i)[j],
						request.form.getlist('month_5_%s' % i)[j],request.form.getlist('month_6_%s' % i)[j],
						request.form.getlist('month_7_%s' % i)[j],request.form.getlist('month_8_%s' % i)[j],
						request.form.getlist('month_9_%s' % i)[j],request.form.getlist('month_10_%s' % i)[j],
						request.form.getlist('month_11_%s' % i)[j],request.form.getlist('month_12_%s' % i)[j],
						request.form.getlist('total_%s' % i)[j],request.form.getlist('pre_month_%s' % i)[j]).add()

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
		return redirect('Process/dqdc/dqdcXed_ysqkfx/%d' % loan_apply_id)

# 打印损益情况分析
@app.route('/Process/dqdc/dy_syb/<int:loan_apply_id>', methods=['GET'])
def dy_syb(loan_apply_id):
		profit_loss = SC_Profit_Loss.query.filter_by(loan_apply_id=loan_apply_id).order_by("id").all()
		count_1 = SC_Profit_Loss.query.filter_by(loan_apply_id=loan_apply_id,items_type=1).count()
		count_3 = SC_Profit_Loss.query.filter_by(loan_apply_id=loan_apply_id,items_type=3).count()
		count_21 = SC_Profit_Loss.query.filter_by(loan_apply_id=loan_apply_id,items_type=21).count()
		count_28 = SC_Profit_Loss.query.filter_by(loan_apply_id=loan_apply_id,items_type=28).count()
		count_29 = SC_Profit_Loss.query.filter_by(loan_apply_id=loan_apply_id,items_type=29).count()
		return render_template("Print/dy_syb.html",loan_apply_id=loan_apply_id,profit_loss=profit_loss,
			count_1=count_1,count_3=count_3,count_21=count_21,count_28=count_28,count_29=count_29)
	