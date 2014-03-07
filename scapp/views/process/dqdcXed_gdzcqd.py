# coding:utf-8
from flask import Module, session, request, render_template, redirect, url_for,flash

from scapp import db
from scapp.config import logger

from scapp.models.credit_data.sc_fixed_assets_estate import SC_Fixed_Assets_Estate
from scapp.models.credit_data.sc_fixed_assets_equipment import SC_Fixed_Assets_Equipment
from scapp.models.credit_data.sc_fixed_assets_car import SC_Fixed_Assets_Car
from scapp.logic.total import AssetsList

from scapp import app

# 贷款调查——小额贷款(固定资产清单)
@app.route('/Process/dqdc/dqdcXed_gdzcqd/<int:id>', methods=['GET'])
def dqdcXed_gdzcqd(id):
	fixed_assets_estate = SC_Fixed_Assets_Estate.query.filter_by(loan_apply_id=id).all()
	fixed_assets_equipment = SC_Fixed_Assets_Equipment.query.filter_by(loan_apply_id=id).all()
	fixed_assets_car = SC_Fixed_Assets_Car.query.filter_by(loan_apply_id=id).all()

	return render_template("Process/dqdc/dqdcXed_gdzcqd.html",id=id,fixed_assets_estate=fixed_assets_estate,
		fixed_assets_equipment=fixed_assets_equipment,fixed_assets_car=fixed_assets_car)

# 贷款调查——新增小额贷款(固定资产清单-房地产)
@app.route('/Process/dqdc/new_fdc/<int:loan_apply_id>', methods=['GET','POST'])
def new_fdc(loan_apply_id):
	if request.method == 'GET':
		return render_template("Process/dqdc/new_fdc.html",loan_apply_id=loan_apply_id)
	else:
		try:
			SC_Fixed_Assets_Estate(loan_apply_id,request.form['name'],request.form['address'],
				request.form['gfa'],request.form['land_area'],request.form['life'],request.form['land_type'],
				request.form['purchase_price'],request.form['price'],request.form['remark']).add()

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

# 贷款调查——编辑小额贷款(固定资产清单-房地产)
@app.route('/Process/dqdc/edit_fdc/<int:id>', methods=['GET','POST'])
def edit_fdc(id):
	if request.method == 'GET':
		fixed_assets_estate = SC_Fixed_Assets_Estate.query.filter_by(id=id).first()
		return render_template("Process/dqdc/edit_fdc.html",fixed_assets_estate=fixed_assets_estate)
	else:
		try:
			fixed_assets_estate = SC_Fixed_Assets_Estate.query.filter_by(id=id).first()
			fixed_assets_estate.name = request.form['name']
			fixed_assets_estate.gfa = request.form['gfa']
			fixed_assets_estate.land_area = request.form['land_area']
			fixed_assets_estate.life = request.form['life']
			fixed_assets_estate.land_type = request.form['land_type']
			fixed_assets_estate.address = request.form['address']
			fixed_assets_estate.purchase_price = request.form['purchase_price']
			fixed_assets_estate.price = request.form['price']
			fixed_assets_estate.remark = request.form['remark']

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

# 贷款调查——新增小额贷款(固定资产清单-设备器材)
@app.route('/Process/dqdc/new_equipment/<int:loan_apply_id>', methods=['GET','POST'])
def new_equipment(loan_apply_id):
	if request.method == 'GET':
		return render_template("Process/dqdc/new_equipment.html",loan_apply_id=loan_apply_id)
	else:
		try:
			SC_Fixed_Assets_Equipment(loan_apply_id,request.form['name'],request.form['amount'],
				request.form['type_brand'],request.form['purchase_date'],request.form['production_date'],
				request.form['total_price'],request.form['price'],request.form['outward'],request.form['remark']).add()

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

# 贷款调查——编辑小额贷款(固定资产清单-设备器材)
@app.route('/Process/dqdc/edit_equipment/<int:id>', methods=['GET','POST'])
def edit_equipment(id):
	if request.method == 'GET':
		fixed_assets_equipment = SC_Fixed_Assets_Equipment.query.filter_by(id=id).first()
		return render_template("Process/dqdc/edit_equipment.html",fixed_assets_equipment=fixed_assets_equipment)
	else:
		try:
			fixed_assets_equipment = SC_Fixed_Assets_Equipment.query.filter_by(id=id).first()
			fixed_assets_equipment.name = request.form['name']
			fixed_assets_equipment.amount = request.form['amount']
			fixed_assets_equipment.type_brand = request.form['type_brand']
			fixed_assets_equipment.purchase_date = request.form['purchase_date']
			fixed_assets_equipment.production_date = request.form['production_date']
			fixed_assets_equipment.total_price = request.form['total_price']
			fixed_assets_equipment.price = request.form['price']
			fixed_assets_equipment.outward = request.form['outward']
			fixed_assets_equipment.remark = request.form['remark']

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

# 贷款调查——新增小额贷款(固定资产清单)
@app.route('/Process/dqdc/new_car', methods=['GET','POST'])
def new_car():
	if request.method == 'GET':
		return render_template("Process/dqdc/new_car.html",loan_apply_id=loan_apply_id)
	else:
		loan_apply_id = request.form['hiddenId']
		assets = AssetsList()
		assets.addList(loan_apply_id,request)
		return redirect('Process/dqdc/dqdcXed_gdzcqd/'+loan_apply_id)