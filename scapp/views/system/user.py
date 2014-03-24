# coding:utf-8
from scapp import db
from scapp.config import PER_PAGE
from scapp.config import logger
import datetime

from flask import Module, session, request, render_template, redirect, url_for, flash
from flask.ext.login import current_user

from scapp.models import SC_User
from scapp.models import SC_Role
from scapp.models import SC_UserRole
from scapp.models import SC_Privilege
from scapp.models import SC_Org
from scapp.models import SC_Application
from scapp.models import SC_Menu

import json
from scapp import app

import hashlib

#get md5 of a input string  
def GetStringMD5(str):  
    m = hashlib.md5()
    m.update(str)
    return m.hexdigest() 

# 使用者管理
@app.route('/System/syzgl/<int:page>', methods=['GET'])
def System_syzgl(page):
	users = SC_User.query.order_by("id").paginate(page, per_page = PER_PAGE)
	return render_template("System/syzgl.html",users=users)
	
# 新增用户
@app.route('/System/new_user', methods=['GET','POST'])
def new_user():
	if request.method == 'GET':
		roles = SC_Role.query.order_by("id").all()
		orgs = SC_Org.query.order_by("id").all()
		leaders = SC_User.query.filter_by(is_leader='1').order_by("id").all()
		return render_template("System/new_user.html",roles=roles,orgs=orgs,leaders=leaders)
	else:
		try:
			if request.form['is_leader'] == '1':
				belong_leader = None
			else:
				if request.form['belong_leader']:
					belong_leader = request.form['belong_leader']
				else:
					belong_leader = None

			user = SC_User(request.form['login_name'],GetStringMD5(request.form['login_password']),
				request.form['real_name'],request.form['sex'],request.form['mobile'],
				request.form['department'],request.form['level'],request.form['active'],
				request.form['is_leader'],belong_leader)
			user.add()

			#清理缓存
			db.session.flush()

			SC_UserRole(user.id,request.form['roles']).add()

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

		return redirect('System/syzgl/1')

# 编辑用户
@app.route('/System/edit_user/<int:id>', methods=['GET','POST'])
def edit_user(id):
	if request.method == 'GET':
		user = SC_User.query.filter_by(id=id).first()
		roles = SC_Role.query.order_by("id").all()
		role = SC_UserRole.query.filter_by(user_id=id).first().role
		orgs = SC_Org.query.order_by("id").all()
		leaders = SC_User.query.filter_by(is_leader='1').order_by("id").all()
		leader = SC_User.query.filter_by(id=user.belong_leader).first()
		return render_template("System/edit_user.html",user=user,roles=roles,role=role,orgs=orgs,
			leaders=leaders,leader=leader)
	else:
		try:
			user = SC_User.query.filter_by(id=id).first()
			user.login_name = request.form['login_name']
			#user.login_password = request.form['login_password']
			user.real_name = request.form['real_name']
			user.sex = request.form['sex']
			user.mobile = request.form['mobile']
			user.department = request.form['department']
			user.level = request.form['level']
			user.active = request.form['active']
			user.is_leader = request.form['is_leader']
			if request.form['is_leader'] == '1':
				user.belong_leader = None
			else:
				if request.form['belong_leader']:
					user.belong_leader = request.form['belong_leader']
				else:
					user.belong_leader = None
			
			user.modify_user = current_user.id
			user.modify_date = datetime.datetime.now()

			user_role = SC_UserRole.query.filter_by(user_id=id).first()
			user_role.role_id = request.form['roles']
			user_role.modify_user = current_user.id
			user_role.modify_date = datetime.datetime.now()

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

		return redirect('System/syzgl/1')
# 用户激活
@app.route('/System/active_user/<int:id>/<int:active>', methods=['GET'])
def active_user(id,active):
    try:
        user = SC_User.query.filter_by(id=id).first()
        user.active = active
        
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

    return redirect('System/syzgl/1')

# 用户激活
@app.route('/System/reset_pwd/<int:id>', methods=['GET'])
def reset_pwd(id):
    try:
        user = SC_User.query.filter_by(id=id).first()
        user.login_password = GetStringMD5('12345')
        
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

    return redirect('System/syzgl/1')

# 角色权限管理
@app.route('/System/jsqxgl/<int:page>', methods=['GET'])
def System_jsqxgl(page):
    # 获取角色并分页
    roles = SC_Role.query.order_by("id").paginate(page, per_page = PER_PAGE)
    return render_template("System/jsqxgl.html",roles = roles)

# 新增角色
@app.route('/System/new_role', methods=['GET','POST'])
def new_role():
	if request.method == 'POST':
		try:
			# 保存角色
			role = SC_Role(request.form['role_name'], request.form['role_level'])
			role.add()
			# 清理缓存 以获得role的对象的id
			db.session.flush()

			# 保存具体权限
			app_tree = SC_Application.query.order_by("id").all()
			for app in app_tree:
				SC_Privilege('SC_Role',role.id,'SC_Application',app.application_code,request.form[app.application_code]).add()
				menu_tree = SC_Menu.query.filter_by(application=app.id).order_by("id").all()
				for menu in menu_tree:
					SC_Privilege('SC_Role',role.id,'SC_Menu',menu.menu_code,request.form[menu.menu_code]).add()

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

		return redirect('System/jsqxgl/1')

	elif request.method == 'GET':
		#读取所有模块
		data = []
		app_tree = SC_Application.query.order_by("id").all()
		for app in app_tree:
			dic = {}
			dic['id'] = app.id
			dic['name'] = app.application_name
			dic['code'] = app.application_code
			app_children = []
			menu_tree = SC_Menu.query.filter_by(application=app.id).order_by("id").all()
			for menu in menu_tree:
				app_children.append({'id':menu.id,'name':menu.menu_name,'code':menu.menu_code})
			dic['children'] = app_children
			data.append(dic)
		return render_template("System/new_role.html",data=data)

# 更新角色
@app.route('/System/edit_role/<int:id>', methods=['GET','POST'])
def edit_role(id):
	if request.method == 'POST':
		try:
			SC_Role.query.filter_by(id=id).update({"role_name":request.form['role_name'],"role_level":request.form['role_level']})

			# 更新权限
			SC_Privilege.query.filter_by(privilege_master='SC_Role',priviliege_master_id=id).delete()
			db.session.flush()

			# 保存具体权限
			app_tree = SC_Application.query.order_by("id").all()
			for app in app_tree:
				SC_Privilege('SC_Role',id,'SC_Application',app.application_code,request.form[app.application_code]).add()
				menu_tree = SC_Menu.query.filter_by(application=app.id).order_by("id").all()
				for menu in menu_tree:
					SC_Privilege('SC_Role',id,'SC_Menu',menu.menu_code,request.form[menu.menu_code]).add()

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

		return redirect('System/jsqxgl/1')

	elif request.method == 'GET':
		role = SC_Role.query.filter_by(id=id).first()
		
		#读取所有模块
		data = []
		app_tree = SC_Application.query.order_by("id").all()
		for app in app_tree:
			dic = {}
			dic['id'] = app.id
			dic['name'] = app.application_name
			dic['code'] = app.application_code
			app_children = []
			menu_tree = SC_Menu.query.filter_by(application=app.id).order_by("id").all()
			for menu in menu_tree:
				app_children.append({'id':menu.id,'name':menu.menu_name,'code':menu.menu_code})
			dic['children'] = app_children
			data.append(dic)
		#获取该role的所有权限
		privileges_app = SC_Privilege.query.filter_by(privilege_master='SC_Role',priviliege_access='SC_Application',
			priviliege_master_id=id).order_by("id").all()
		privileges_menu = SC_Privilege.query.filter_by(privilege_master='SC_Role',priviliege_access='SC_Menu',
			priviliege_master_id=id).order_by("id").all()

		return render_template("System/edit_role.html",role=role,data=data,privileges_app=privileges_app,
			privileges_menu=privileges_menu)