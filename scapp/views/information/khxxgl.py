# coding:utf-8

import os

from werkzeug import secure_filename
from flask import Module, session, request, render_template, redirect, url_for,flash
from flask.ext.login import login_user, logout_user, current_user, login_required
import datetime

from scapp import db
from scapp.config import logger
from scapp.config import PER_PAGE
from scapp.config import UPLOAD_FOLDER_REL
from scapp.config import UPLOAD_FOLDER_ABS

from scapp.models import SC_Target_Customer
from scapp.models import SC_Individual_Customer
from scapp.models import SC_Company_Customer
from scapp.models import SC_Dealings
from scapp.models import SC_Relations
from scapp.models import SC_Manage_Info
from scapp.models import SC_Asset_Info
from scapp.models import SC_Other_Info
from scapp.models import SC_Financial_Affairs
from scapp.models import SC_User
from scapp.models import SC_Org

from scapp.models import SC_Credentials_Type
from scapp.models import SC_Regisiter_Type
from scapp.models import SC_Relation_Type
from scapp.models import SC_Industry
from scapp.models import SC_Business_Type
from scapp.models import SC_Asset_Type

from scapp import app

# 客户信息管理
@app.route('/Information/khxxgl', methods=['GET'])
def Information_khxxgl():
    org = SC_Org.query.order_by("id").all()
    return render_template("Information/khxxgl_search.html",org=org)
	
# 客户信息搜索
@app.route('/Information/khxxgl_search/<int:page>', methods=['GET','POST'])
def khxxgl_search(page):
	# 个人
	if request.form['customer_type'] == 'Individual':
		individual_customer = SC_Individual_Customer.query.order_by("id").paginate(page, per_page = PER_PAGE)
		return render_template("Information/khxxgl.html",customer=individual_customer)
	# 公司
	else:
		company_customer = SC_Company_Customer.query.order_by("id").paginate(page, per_page = PER_PAGE)
		return render_template("Information/khxxgl.html",customer=company_customer)

# 跳转到新增客户页面
@app.route('/Information/new_customer/<int:target_customer_id>', methods=['GET','POST'])
def new_customer(target_customer_id):
	if request.method == 'POST':
		customer_type = request.form['customer_type']
		target_customer_id = request.form['manager']
		if customer_type == 'Company' :
			return redirect('Information/new_company_customer/%s' % target_customer_id)
		if customer_type == 'Individual' :
			return redirect('Information/new_individual_customer/%s' % target_customer_id)
		
	else:
		target_customer = SC_Target_Customer.query.filter_by(loan_officer=current_user.id).order_by("id").all()
		return render_template("Information/new_customer.html",target_customer_id=target_customer_id,
			target_customer=target_customer)

# 客户基本信息——公司类
@app.route('/Information/new_company_customer/<int:target_customer_id>',methods=['GET','POST'])
def new_company_customer(target_customer_id):
	if request.method == 'POST':
		try:
			SC_Company_Customer(current_user.id,request.form['customer_no'],request.form['customer_name'],
				request.form['frdb'],request.form['yyzz'],request.form['yyzz_fzjg'],request.form['swdjz'],
				request.form['swdjz_fzjg'],request.form['gszczj'],request.form['gsyyfw'],request.form['gsclrq'],
				request.form['gszclx'],request.form['jbhzh'],request.form['zcdz'],request.form['xdz'],request.form['bgdz'],
				request.form['qtdz'],request.form['education'],request.form['family'],request.form['telephone'],
				request.form['mobile'],request.form['contact_phone'],request.form['email']).add()

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
			
		return redirect('Information/khxxgl')

	else:	
		target_customer = SC_Target_Customer.query.filter_by(id=target_customer_id).first()
		user = SC_User.query.order_by("id").all()
		regisiter_type = SC_Regisiter_Type.query.order_by("id").all()

		return render_template("Information/new_company_customer.html",user=user,
			regisiter_type=regisiter_type,target_customer=target_customer)

# 客户基本信息——个人类
@app.route('/Information/new_individual_customer/<int:target_customer_id>', methods=['GET','POST'])
def new_individual_customer(target_customer_id):
	if request.method == 'POST':
		try:
			is_otherjob = request.form['is_otherjob']
			profession = None
			duty = None
			title = None
			if is_otherjob =='1':
			    profession = request.form['profession']
			    duty = request.form['duty']
			    title = request.form['title']

			SC_Individual_Customer(current_user.id,request.form['customer_no'],request.form['customer_name'],
			    request.form['birthday'],request.form['sex'],request.form['credentials_type'],request.form['credentials_no'],
			    request.form['degree'],request.form['education'],request.form['marriage'],request.form['telephone'],
			    request.form['mobile'],request.form['residence'],request.form['residence_address'],request.form['home_address'],
			    request.form['zip_code'],request.form['families'],request.form['living_conditions'],
			    is_otherjob,profession,duty,title,
			    request.form['name_1'],request.form['relationship_1'],request.form['phone_1'],
			    request.form['name_2'],request.form['relationship_2'],request.form['phone_2'],
			    request.form['name_3'],request.form['relationship_3'],request.form['phone_3'],
			    request.form['name_4'],request.form['relationship_4'],request.form['phone_4'],
			    request.form['spouse_name'],request.form['spouse_company'],request.form['spouse_credentials_type'],
			    request.form['spouse_credentials_no'],request.form['spouse_phone'],request.form['spouse_mobile']).add()

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

		return redirect('Information/khxxgl')

	else:
		target_customer = SC_Target_Customer.query.filter_by(id=target_customer_id).first()
		user = SC_User.query.order_by("id").all()
		credentials_type = SC_Credentials_Type.query.order_by("id").all()

		return render_template("Information/new_individual_customer.html",user=user,
		    credentials_type=credentials_type,target_customer=target_customer)

# 编辑客户--公司
@app.route('/Information/edit_company/<int:id>', methods=['GET'])
def edit_company(id):
	customer = SC_Company_Customer.query.filter_by(id=id).first()
	return render_template("Information/edit_company.html",customer=customer)

# 编辑客户--个人
@app.route('/Information/edit_individual/<int:id>', methods=['GET'])
def edit_individual(id):
	customer = SC_Individual_Customer.query.filter_by(id=id).first()
	return render_template("Information/edit_individual.html",customer=customer)
	
# 编辑客户基本信息--公司
@app.route('/Information/edit_company_customer/<int:id>', methods=['GET','POST'])
def edit_company_customer(id):
	if request.method == 'POST':
		try:
			customer = SC_Company_Customer.query.filter_by(id=id).first()

			customer.manager = current_user.id
			customer.customer_no = request.form['customer_no']
			customer.customer_name = request.form['customer_name']
			customer.frdb = request.form['frdb']
			customer.yyzz = request.form['yyzz']
			customer.yyzz_fzjg = request.form['yyzz_fzjg']
			customer.swdjz = request.form['swdjz']
			customer.swdjz_fzjg = request.form['swdjz_fzjg']
			customer.gszczj = request.form['gszczj']
			customer.gsyyfw = request.form['gsyyfw']
			customer.gsclrq = request.form['gsclrq']
			customer.gszclx = request.form['gszclx']
			customer.jbhzh = request.form['jbhzh']
			customer.zcdz = request.form['zcdz']
			customer.xdz = request.form['xdz']
			customer.bgdz = request.form['bgdz']
			customer.qtdz = request.form['qtdz']
			customer.education = request.form['education']
			customer.family = request.form['family']
			customer.telephone = request.form['telephone']
			customer.mobile = request.form['mobile']
			customer.contact_phone = request.form['contact_phone']
			customer.email = request.form['email']
			customer.is_active = request.form['is_active']

			customer.modify_user = current_user.id
			customer.modify_date = datetime.datetime.now()

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

		return redirect('xxgl')

	else:
		customer = SC_Company_Customer.query.filter_by(id=id).first()

		regisiter_type = SC_Regisiter_Type.query.order_by("id").all()

		return render_template("Information/edit_company_customer.html",customer=customer,
			regisiter_type=regisiter_type)

# 编辑客户基本信息--个人
@app.route('/Information/edit_individual_customer/<int:id>', methods=['GET','POST'])
def edit_individual_customer(id):
	if request.method == 'POST':
		try:
			customer = SC_Individual_Customer.query.filter_by(id=id).first()

			customer.manager=current_user.id
			customer.customer_no=request.form['customer_no']
			customer.customer_name=request.form['customer_name']
			customer.birthday=request.form['birthday']
			customer.sex=request.form['sex']
			customer.credentials_type=request.form['credentials_type']
			customer.credentials_no=request.form['credentials_no']
			customer.degree=request.form['degree']
			customer.education=request.form['education']
			customer.marriage=request.form['marriage']
			customer.telephone=request.form['telephone']
			customer.mobile=request.form['mobile']
			customer.residence=request.form['residence']
			customer.residence_address=request.form['residence_address']
			customer.home_address=request.form['home_address']
			customer.zip_code=request.form['zip_code']
			customer.families=request.form['families']
			customer.living_conditions=request.form['living_conditions']
			customer.is_otherjob=request.form['is_otherjob']
			if request.form['is_otherjob'] == '1':
			    customer.profession=request.form['profession']
			    customer.duty=request.form['duty']
			    customer.title=request.form['title']
			else:
			    customer.profession=None
			    customer.duty=None
			    customer.title=None
                            
			customer.name_1=request.form['name_1']
			customer.relationship_1=request.form['relationship_1']
			customer.phone_1=request.form['phone_1']
			customer.name_2=request.form['name_2']
			customer.relationship_2=request.form['relationship_2']
			customer.phone_2=request.form['phone_2']
			customer.name_3=request.form['name_3']
			customer.relationship_3=request.form['relationship_3']
			customer.phone_3=request.form['phone_3']
			customer.name_4=request.form['name_4']
			customer.relationship_4=request.form['relationship_4']
			customer.phone_4=request.form['phone_4']
			customer.spouse_name=request.form['spouse_name']
			customer.spouse_company=request.form['spouse_company']
			customer.spouse_credentials_type=request.form['spouse_credentials_type']
			customer.spouse_credentials_no=request.form['spouse_credentials_no']
			customer.spouse_phone=request.form['spouse_phone']
			customer.spouse_mobile=request.form['spouse_mobile']
			#customer.is_active=request.form['is_active']

			customer.modify_user = current_user.id
			customer.modify_date = datetime.datetime.now()

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

		return redirect('xxgl')

	else:
		customer = SC_Individual_Customer.query.filter_by(id=id).first()

		credentials_type = SC_Credentials_Type.query.order_by("id").all()

		return render_template("Information/edit_individual_customer.html",customer=customer,
			credentials_type=credentials_type)

# 编辑客户--行业务往来信息
@app.route('/Information/sc_dealings/<belong_customer_type>/<int:belong_customer_value>', methods=['GET','POST'])
def sc_dealings(belong_customer_type,belong_customer_value):
	if request.method == 'POST':
		try:
			SC_Dealings(request.form['deal_name'],request.form['deal_description'],
				belong_customer_type,belong_customer_value).add()

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

		return redirect('xxgl')

	else:
		dealings = SC_Dealings.query.filter_by(belong_customer_type=belong_customer_type,
			belong_customer_value=belong_customer_value).order_by("id").all()
		if belong_customer_type == 'Company':
			customer = SC_Company_Customer.query.filter_by(id=belong_customer_value).first()
			return render_template("Information/sc_dealings.html",customer=customer,dealings=dealings)
		else:
			customer = SC_Individual_Customer.query.filter_by(id=belong_customer_value).first()
			return render_template("Information/sc_dealings.html",customer=customer,dealings=dealings)
		

# 编辑客户--关系人信息
@app.route('/Information/sc_relations/<belong_customer_type>/<int:belong_customer_value>', methods=['GET','POST'])
def sc_relations(belong_customer_type,belong_customer_value):
	if request.method == 'POST':
		try:
			SC_Relations(request.form['relation_no'],request.form['relation_name'],
				request.form['relation_type'],request.form['cgbl'],request.form['business_name'],
				request.form['relation_describe'],belong_customer_type,belong_customer_value).add()

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

		return redirect('xxgl')

	else:
		if belong_customer_type == 'Company':
			customer = SC_Company_Customer.query.filter_by(id=belong_customer_value).first()
			return render_template("Information/sc_relations.html",customer=customer)
		else:
			customer = SC_Individual_Customer.query.filter_by(id=belong_customer_value).first()
			return render_template("Information/sc_relations.html",customer=customer)

# 编辑客户--经营信息
@app.route('/Information/sc_manage_info/<belong_customer_type>/<int:belong_customer_value>', methods=['GET','POST'])
def sc_manage_info(belong_customer_type,belong_customer_value):
	if request.method == 'POST':
		try:
			SC_Manage_Info(request.form['business_name'],request.form['industry'],
				request.form['business_description'],request.form['business_type'],request.form['stake'],
				request.form['business_address'],request.form['annual_income'],request.form['monthly_income'],
				request.form['establish_date'],request.form['employees'],request.form['manager_name'],
				request.form['credentials_type'],request.form['credentials_no'],request.form['credentials_org'],
				belong_customer_type,belong_customer_value).add()

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
			
		return redirect('xxgl')

	else:
		credentials_type = SC_Credentials_Type.query.order_by("id").all()
		industry = SC_Industry.query.order_by("id").all()
		business_type = SC_Business_Type.query.order_by("id").all()
		manege_info = SC_Manage_Info.query.filter_by(belong_customer_type=belong_customer_type,
			belong_customer_value=belong_customer_value).order_by("id").all()
		if belong_customer_type == 'Company':
			customer = SC_Company_Customer.query.filter_by(id=belong_customer_value).first()
			return render_template("Information/sc_manage_info.html",customer=customer,credentials_type=credentials_type,
				industry=industry,business_type=business_type,manege_info=manege_info)
		else:
			customer = SC_Individual_Customer.query.filter_by(id=belong_customer_value).first()
			return render_template("Information/sc_manage_info.html",customer=customer,credentials_type=credentials_type,
				industry=industry,business_type=business_type,manege_info=manege_info)

# 编辑客户--资产信息
@app.route('/Information/sc_asset_info/<belong_customer_type>/<int:belong_customer_value>', methods=['GET','POST'])
def sc_asset_info(belong_customer_type,belong_customer_value):
	if request.method == 'POST':
		try:
			SC_Asset_Info(request.form['asset_name'],request.form['asset_type'],
				request.form['asset_description'],request.form['asset_position'],request.form['credentials_name'],
				request.form['credentials_no'],request.form['appraisal'],request.form['is_mortgage'],
				request.form['mortgage_amount'],request.form['mortgage_object'],
				belong_customer_type,belong_customer_value).add()

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

		return redirect('xxgl')

	else:
		asset_type = SC_Asset_Type.query.order_by("id").all()
		asset_info = SC_Asset_Info.query.filter_by(belong_customer_type=belong_customer_type,
			belong_customer_value=belong_customer_value).order_by("id").all()
		if belong_customer_type == 'Company':
			customer = SC_Company_Customer.query.filter_by(id=belong_customer_value).first()
			return render_template("Information/sc_asset_info.html",customer=customer,asset_type=asset_type,
				asset_info=asset_info)
		else:
			customer = SC_Individual_Customer.query.filter_by(id=belong_customer_value).first()
			return render_template("Information/sc_asset_info.html",customer=customer,asset_type=asset_type,
				asset_info=asset_info)
		
# 编辑客户--财务信息
@app.route('/Information/sc_financial_affairs/<belong_customer_type>/<int:belong_customer_value>', methods=['GET','POST'])
def sc_financial_affairs(belong_customer_type,belong_customer_value):
	if request.method == 'POST':
		try:
			SC_Financial_Affairs(request.form['main_supplier'],request.form['main_client'],
				request.form['total_assets'],request.form['stock'],request.form['accounts'],
				request.form['fixed_assets'],request.form['total_liabilities'],request.form['bank_borrowings'],
				request.form['private_borrowers'],request.form['monthly_sales'],request.form['profit'],
				request.form['other_monthly_income'],belong_customer_type,belong_customer_value).add()
				
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

		return redirect('xxgl')

	else:
		financial_affairs = SC_Financial_Affairs.query.filter_by(belong_customer_type=belong_customer_type,
			belong_customer_value=belong_customer_value).order_by("id").first()

		if belong_customer_type == 'Company':
			customer = SC_Company_Customer.query.filter_by(id=belong_customer_value).first()
			return render_template("Information/sc_financial_affairs.html",customer=customer,financial_affairs=financial_affairs)
		else:
			customer = SC_Individual_Customer.query.filter_by(id=belong_customer_value).first()
			return render_template("Information/sc_financial_affairs.html",customer=customer,financial_affairs=financial_affairs)

# 编辑客户--附加信息
@app.route('/Information/sc_other_info/<belong_customer_type>/<int:belong_customer_value>', methods=['GET','POST'])
def sc_other_info(belong_customer_type,belong_customer_value):
	if request.method == 'POST':
		try:
			# 先获取上传文件
			f = request.files['attachment']
			fname = f.filename
			f.save(os.path.join(UPLOAD_FOLDER_ABS, fname))

			SC_Other_Info(request.form['info_name'],request.form['info_description'],
				UPLOAD_FOLDER_REL + fname,belong_customer_type,belong_customer_value).add()

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

		return redirect('xxgl')

	else:
		other_info = SC_Other_Info.query.filter_by(belong_customer_type=belong_customer_type,
			belong_customer_value=belong_customer_value).order_by("id").all()
		if belong_customer_type == 'Company':
			customer = SC_Company_Customer.query.filter_by(id=belong_customer_value).first()
			return render_template("Information/sc_other_info.html",customer=customer,other_info=other_info)
		else:
			customer = SC_Individual_Customer.query.filter_by(id=belong_customer_value).first()
			return render_template("Information/sc_other_info.html",customer=customer,other_info=other_info)