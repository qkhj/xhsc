# coding:utf-8
from flask import Module, session, request, render_template, redirect, url_for,flash

from scapp import db
from scapp.config import logger

from scapp.models.credit_data.sc_cross_examination import SC_Cross_Examination
from scapp.models.credit_data.sc_balance_sheet import SC_Balance_Sheet
from scapp.models.credit_data.sc_profit_jcjy import SC_Profit_Jcjy

from scapp import app

# 贷款调查——小额贷款(交叉检验)
@app.route('/Process/dqdc/dqdcXed_jcjy/<int:loan_apply_id>', methods=['GET','POST'])
def dqdcXed_jcjy(loan_apply_id):
	if request.method == 'GET':
		cross_examination = SC_Cross_Examination.query.filter_by(loan_apply_id=loan_apply_id).order_by("id").all()
		count_3 = SC_Cross_Examination.query.filter_by(loan_apply_id=loan_apply_id,loan_type=3).count()
		balance_sheet = SC_Balance_Sheet.query.filter_by(loan_apply_id=loan_apply_id,loan_type=16).first()#type=16为资产负债表中的所有者权益
		
		#查询毛利润详细信息
		profit_jcjy = SC_Profit_Jcjy.query.filter_by(loan_apply_id=loan_apply_id).order_by("id").all()
		maxIndex = -1;
		for obj in profit_jcjy:
			if obj.index is not None and obj.index > maxIndex:
				maxIndex = obj.index
		
		return render_template("Process/dqdc/dqdcXed_jcjy.html",loan_apply_id=loan_apply_id,
			cross_examination=cross_examination,count_3=count_3,balance_sheet=balance_sheet,
			profit_jcjy=profit_jcjy,maxIndex=maxIndex)
	else:
		try:
			SC_Cross_Examination.query.filter_by(loan_apply_id=loan_apply_id).delete()
			db.session.flush()

			for i in range(15):
				for j in range(len(request.form.getlist('type_%s' % i))):
					SC_Cross_Examination(loan_apply_id,i,request.form.getlist('name_%s' % i)[j],
						j,request.form.getlist('value_%s' % i)[j]).add()
						
			#修改毛利润录入方式
			SC_Profit_Jcjy.query.filter_by(loan_apply_id=loan_apply_id).delete()
			db.session.flush()
			
			if request.form['record_type'] == '2':#录入详细数据
				names = request.form.getlist('name')
				types = request.form.getlist('type')
				bids = request.form.getlist('bid')
				prices = request.form.getlist('price')
				ratios = request.form.getlist('ratio')
				profits = request.form.getlist('profit')
				
				index1 = -1#递增序列
				index2 = -1#递增序列
				for i in range(len(names)):
					if types[i] == '1':
						index1 = index1 + 1
						index = index1
					if types[i] == '2':
						index = index1
					if types[i] == '3':
						index2 = index2 + 1
						index = index2
					if types[i] == '4':
						index = None
					SC_Profit_Jcjy(loan_apply_id,types[i],index,names[i],bids[i],prices[i],ratios[i],profits[i]).add()
				
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

		return redirect('Process/dqdc/dqdcXed_jcjy/%d' % loan_apply_id)

# 打印交叉检验
@app.route('/Process/dqdc/dy_jcjy/<int:loan_apply_id>', methods=['GET'])
def dy_jcjy(loan_apply_id):
	cross_examination = SC_Cross_Examination.query.filter_by(loan_apply_id=loan_apply_id).order_by("id").all()
	count_3 = SC_Cross_Examination.query.filter_by(loan_apply_id=loan_apply_id,loan_type=3).count()
	balance_sheet = SC_Balance_Sheet.query.filter_by(loan_apply_id=loan_apply_id,loan_type=16).first()#type=16为资产负债表中的所有者权益
	
	#查询毛利润详细信息
	profit_jcjy = SC_Profit_Jcjy.query.filter_by(loan_apply_id=loan_apply_id).order_by("id").all()
	maxIndex = -1;
	for obj in profit_jcjy:
		if obj.index is not None and obj.index > maxIndex:
			maxIndex = obj.index
				
	return render_template("Print/dy_jcjy.html",loan_apply_id=loan_apply_id,
		cross_examination=cross_examination,count_3=count_3,balance_sheet=balance_sheet,
		profit_jcjy=profit_jcjy,maxIndex=maxIndex)