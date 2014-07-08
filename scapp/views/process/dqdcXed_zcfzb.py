# coding:utf-8
from flask import Module, session, request, render_template, redirect, url_for,flash

import os
import datetime
from scapp import db
from scapp.config import logger

from scapp.config import APPY_FOLDER_REL
from scapp.config import APPY_FOLDER_ABS
from scapp.config import unopath
from scapp.config import openofficepath

from scapp.models.credit_data.sc_stock import SC_Stock
import json
from scapp.helpers import AlchemyEncoder

from scapp.models.credit_data.sc_balance_sheet import SC_Balance_Sheet

from scapp import app

#from appy.pod.renderer import Renderer

staff = [{'firstName': 'Delannay', 'name': 'Gaetan', 'age': 112},
		{'firstName': 'Gauthier', 'name': 'Bastien', 'age': 5},
		{'firstName': 'Jean-Michel', 'name': 'Abe', 'age': 79}]

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
			
		return redirect('Process/dqdc/dqdcXed_zcfzb/%d' % loan_apply_id)

@app.route('/Process/dqdc/dy_fcw/<int:loan_apply_id>', methods=['GET'])
def dqdcXed_fcw_dy(loan_apply_id):
	balance_sheets = SC_Balance_Sheet.query.filter_by(loan_apply_id=loan_apply_id).order_by("id").all()
	count_0 = SC_Balance_Sheet.query.filter_by(loan_apply_id=loan_apply_id,loan_type=0).count()
	count_2 = SC_Balance_Sheet.query.filter_by(loan_apply_id=loan_apply_id,loan_type=2).count()
	count_4 = SC_Balance_Sheet.query.filter_by(loan_apply_id=loan_apply_id,loan_type=4).count()
	count_6 = SC_Balance_Sheet.query.filter_by(loan_apply_id=loan_apply_id,loan_type=6).count()
	count_10 = SC_Balance_Sheet.query.filter_by(loan_apply_id=loan_apply_id,loan_type=10).count()
	count_12 = SC_Balance_Sheet.query.filter_by(loan_apply_id=loan_apply_id,loan_type=12).count()
	return render_template("Print/dy_fcwqkfx.html",loan_apply_id=loan_apply_id,
		balance_sheets=balance_sheets,count_0=count_0,count_2=count_2,count_4=count_4,count_6=count_6,
		count_10=count_10,count_12=count_12)

@app.route('/Process/dqdc/dy_zcfzb/<int:loan_apply_id>', methods=['GET'])
def dqdcXed_zcfzb_dy(loan_apply_id):
	balance_sheets = SC_Balance_Sheet.query.filter_by(loan_apply_id=loan_apply_id).order_by("id").all()
	count_0 = SC_Balance_Sheet.query.filter_by(loan_apply_id=loan_apply_id,loan_type=0).count()
	count_2 = SC_Balance_Sheet.query.filter_by(loan_apply_id=loan_apply_id,loan_type=2).count()
	count_4 = SC_Balance_Sheet.query.filter_by(loan_apply_id=loan_apply_id,loan_type=4).count()
	count_6 = SC_Balance_Sheet.query.filter_by(loan_apply_id=loan_apply_id,loan_type=6).count()
	count_10 = SC_Balance_Sheet.query.filter_by(loan_apply_id=loan_apply_id,loan_type=10).count()
	count_12 = SC_Balance_Sheet.query.filter_by(loan_apply_id=loan_apply_id,loan_type=12).count()
	return render_template("Print/dy_zcfzb.html",loan_apply_id=loan_apply_id,
		balance_sheets=balance_sheets,count_0=count_0,count_2=count_2,count_4=count_4,count_6=count_6,
		count_10=count_10,count_12=count_12)


def appypdf(loan_apply_id):

	#data = SC_Balance_Sheet.query.filter_by(loan_apply_id=loan_apply_id,loan_type=8).all()
	
	#gen
	now_time = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
	target_file = now_time + ".odt"
	print locals()
	renderer = Renderer(os.path.join(APPY_FOLDER_ABS,'simple11.odt'), globals(),os.path.join(APPY_FOLDER_ABS,target_file),pythonWithUnoPath=openofficepath)
	renderer.run()
	#download
	return redirect(url_for('static', filename='appy/' + target_file), code=301)

def callWS(loan_apply_id):
	data=SC_Stock.query.filter_by(loan_apply_id=loan_apply_id).all()

	from suds.client import Client
	url = 'http://192.168.0.250:9000/ws/hello?wsdl'
	client = Client(url)
	ret = client.service.sayHello(json.dumps(data,cls=AlchemyEncoder,ensure_ascii=False))
	print ret

