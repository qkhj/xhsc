# coding:utf-8
from scapp import db
from scapp.config import logger

from flask import Module, session, request, render_template, redirect, url_for, flash

from scapp.models.information import SC_Credentials_Type
from scapp.models.information import SC_Relation_Type
from scapp.models.information import SC_Industry
from scapp.models.information import SC_Regisiter_Type
from scapp.models.information import SC_Business_Type
from scapp.models.information import SC_Asset_Type
from scapp.models.information import SC_Loan_Purpose
from scapp.models.information import SC_Risk_Level

from scapp import app

# 数据字典
@app.route('/System/sjzd', methods=['GET'])
def System_sjzd():
    # 获取所有字典
    credentials_type = SC_Credentials_Type.query.order_by("id").all()
    relation_Type = SC_Relation_Type.query.order_by("id").all()
    industry = SC_Industry.query.order_by("id").all()
    regisiter_type = SC_Regisiter_Type.query.order_by("id").all()
    business_type = SC_Business_Type.query.order_by("id").all()
    asset_type = SC_Asset_Type.query.order_by("id").all()
    loan_purpose = SC_Loan_Purpose.query.order_by("id").all()
    risk_level = SC_Risk_Level.query.order_by("id").all()

    return render_template("System/sjzd.html", credentials_type=credentials_type
        , relation_Type=relation_Type, industry=industry
        , regisiter_type=regisiter_type, business_type=business_type, asset_type=asset_type
        , loan_purpose=loan_purpose,risk_level=risk_level)
		
# 新增数据字典
@app.route('/System/new_sjzd/<tablename>', methods=['GET','POST'])
def new_sjzd(tablename):
	if request.method == 'POST':
		try:
			if tablename != 'SC_Risk_Level':
				eval(tablename+'(\''+request.form['type_name']+'\')').add()
			else:
				eval(tablename+'(\''+request.form['type_name']+'\',\''+request.form['type_value']+'\')').add()

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

		return redirect('System/sjzd')
	else:
		return render_template("System/new_sjzd.html",tablename=tablename)

# 更新数据字典
@app.route('/System/edit_sjzd/<tablename>/<int:id>', methods=['GET','POST'])
def edit_sjzd(tablename,id):
	if request.method == 'POST':
		try:
			obj = eval(tablename).query.filter_by(id=id).first()
			obj.type_name = request.form['type_name']
			if tablename == 'SC_Risk_Level':
				obj.type_value = request.form['type_value']

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

		return redirect('System/sjzd')
	else:
		obj = eval(tablename).query.filter_by(id=id).first()
		return render_template("System/edit_sjzd.html",tablename=tablename,obj=obj)