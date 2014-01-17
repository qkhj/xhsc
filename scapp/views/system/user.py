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

from scapp import app

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
		return render_template("System/new_user.html",roles=roles,orgs=orgs)
	else:
		try:
			user = SC_User(request.form['login_name'],request.form['login_password'],
				request.form['real_name'],request.form['sex'],request.form['mobile'],
				request.form['department'],request.form['level'],request.form['active'])
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
		return render_template("System/edit_user.html",user=user,roles=roles,role=role,orgs=orgs)
	else:
		try:
			user = SC_User.query.filter_by(id=id).first()
			user.login_name = request.form['login_name']
			user.login_password = request.form['login_password']
			user.real_name = request.form['real_name']
			user.sex = request.form['sex']
			user.mobile = request.form['mobile']
			user.department = request.form['department']
			user.level = request.form['level']
			user.active = request.form['active']
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
        user.login_password = '12345'
        
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
#			SC_Privilege(role.id,'xxgl',request.form['xxgl']).add()
#			SC_Privilege(role.id,'khxxgl',request.form['khxxgl']).add()
#			SC_Privilege(role.id,'dkxxgl',request.form['dkxxgl']).add()
#			SC_Privilege(role.id,'lcgl',request.form['lcgl']).add()
#			SC_Privilege(role.id,'lfdj',request.form['lfdj']).add()
#			SC_Privilege(role.id,'dksq',request.form['dksq']).add()
#			SC_Privilege(role.id,'dksqsh',request.form['dksqsh']).add()
#			SC_Privilege(role.id,'dqdc',request.form['dqdc']).add()
#			SC_Privilege(role.id,'dksp',request.form['dksp']).add()
#			SC_Privilege(role.id,'dkfk',request.form['dkfk']).add()
#			SC_Privilege(role.id,'fksh',request.form['fksh']).add()
#			SC_Privilege(role.id,'hkdj',request.form['hkdj']).add()
#			SC_Privilege(role.id,'dhbg',request.form['dhbg']).add()
#			SC_Privilege(role.id,'dhbgsh',request.form['dhbgsh']).add()
#			SC_Privilege(role.id,'dhgl',request.form['dhgl']).add()
#			SC_Privilege(role.id,'zcfl',request.form['zcfl']).add()
#			SC_Privilege(role.id,'zcflsh',request.form['zcflsh']).add()
#			SC_Privilege(role.id,'xtgj',request.form['xtgj']).add()
#			SC_Privilege(role.id,'hkjhjsgj',request.form['hkjhjsgj']).add()
#			SC_Privilege(role.id,'xtgl',request.form['xtgl']).add()
#			SC_Privilege(role.id,'ywcspz',request.form['ywcspz']).add()
#			SC_Privilege(role.id,'jkpz',request.form['jkpz']).add()
#			SC_Privilege(role.id,'rzrj',request.form['rzrj']).add()
#			SC_Privilege(role.id,'sjzd',request.form['sjzd']).add()
#			SC_Privilege(role.id,'jggl',request.form['jggl']).add()
#			SC_Privilege(role.id,'syzgl',request.form['syzgl']).add()
#			SC_Privilege(role.id,'jsqxgl',request.form['jsqxgl']).add()
#			SC_Privilege(role.id,'tjbb',request.form['tjbb']).add()
#			SC_Privilege(role.id,'kh',request.form['kh']).add()
#			SC_Privilege(role.id,'dkgjztfl',request.form['dkgjztfl']).add()
#			SC_Privilege(role.id,'xdgzlclb',request.form['xdgzlclb']).add()
#			SC_Privilege(role.id,'pcscbbcx',request.form['pcscbbcx']).add()
#			SC_Privilege(role.id,'zhgllbb',request.form['zhgllbb']).add()

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
		return render_template("System/new_role.html")

# 更新角色
@app.route('/System/edit_role/<int:id>', methods=['GET','POST'])
def edit_role(id):
	if request.method == 'POST':
		try:
			SC_Role.query.filter_by(id=id).update({"role_name":request.form['role_name'],"role_level":request.form['role_level']})

			# 更新权限
#			SC_Privilege.query.filter_by(priviliege_master_id=id,priviliege_access='xxgl').update({"priviliege_operation":request.form['xxgl']})
#			SC_Privilege.query.filter_by(priviliege_master_id=id,priviliege_access='khxxgl').update({"priviliege_operation":request.form['khxxgl']})
#			SC_Privilege.query.filter_by(priviliege_master_id=id,priviliege_access='dkxxgl').update({"priviliege_operation":request.form['dkxxgl']})
#			SC_Privilege.query.filter_by(priviliege_master_id=id,priviliege_access='lcgl').update({"priviliege_operation":request.form['lcgl']})
#			SC_Privilege.query.filter_by(priviliege_master_id=id,priviliege_access='lfdj').update({"priviliege_operation":request.form['lfdj']})
#			SC_Privilege.query.filter_by(priviliege_master_id=id,priviliege_access='dksq').update({"priviliege_operation":request.form['dksq']})
#			SC_Privilege.query.filter_by(priviliege_master_id=id,priviliege_access='dksqsh').update({"priviliege_operation":request.form['dksqsh']})
#			SC_Privilege.query.filter_by(priviliege_master_id=id,priviliege_access='dqdc').update({"priviliege_operation":request.form['dqdc']})
#			SC_Privilege.query.filter_by(priviliege_master_id=id,priviliege_access='dksp').update({"priviliege_operation":request.form['dksp']})
#			SC_Privilege.query.filter_by(priviliege_master_id=id,priviliege_access='dkfk').update({"priviliege_operation":request.form['dkfk']})
#			SC_Privilege.query.filter_by(priviliege_master_id=id,priviliege_access='fksh').update({"priviliege_operation":request.form['fksh']})
#			SC_Privilege.query.filter_by(priviliege_master_id=id,priviliege_access='hkdj').update({"priviliege_operation":request.form['hkdj']})
#			SC_Privilege.query.filter_by(priviliege_master_id=id,priviliege_access='dhbg').update({"priviliege_operation":request.form['dhbg']})
#			SC_Privilege.query.filter_by(priviliege_master_id=id,priviliege_access='dhbgsh').update({"priviliege_operation":request.form['dhbgsh']})
#			SC_Privilege.query.filter_by(priviliege_master_id=id,priviliege_access='dhgl').update({"priviliege_operation":request.form['dhgl']})
#			SC_Privilege.query.filter_by(priviliege_master_id=id,priviliege_access='zcfl').update({"priviliege_operation":request.form['zcfl']})
#			SC_Privilege.query.filter_by(priviliege_master_id=id,priviliege_access='zcflsh').update({"priviliege_operation":request.form['zcflsh']})
#			SC_Privilege.query.filter_by(priviliege_master_id=id,priviliege_access='xtgj').update({"priviliege_operation":request.form['xtgj']})
#			SC_Privilege.query.filter_by(priviliege_master_id=id,priviliege_access='hkjhjsgj').update({"priviliege_operation":request.form['hkjhjsgj']})
#			SC_Privilege.query.filter_by(priviliege_master_id=id,priviliege_access='xtgl').update({"priviliege_operation":request.form['xtgl']})
#			SC_Privilege.query.filter_by(priviliege_master_id=id,priviliege_access='ywcspz').update({"priviliege_operation":request.form['ywcspz']})
#			SC_Privilege.query.filter_by(priviliege_master_id=id,priviliege_access='jkpz').update({"priviliege_operation":request.form['jkpz']})
#			SC_Privilege.query.filter_by(priviliege_master_id=id,priviliege_access='rzrj').update({"priviliege_operation":request.form['rzrj']})
#			SC_Privilege.query.filter_by(priviliege_master_id=id,priviliege_access='sjzd').update({"priviliege_operation":request.form['sjzd']})
#			SC_Privilege.query.filter_by(priviliege_master_id=id,priviliege_access='jggl').update({"priviliege_operation":request.form['jggl']})
#			SC_Privilege.query.filter_by(priviliege_master_id=id,priviliege_access='syzgl').update({"priviliege_operation":request.form['syzgl']})
#			SC_Privilege.query.filter_by(priviliege_master_id=id,priviliege_access='jsqxgl').update({"priviliege_operation":request.form['jsqxgl']})
#			SC_Privilege.query.filter_by(priviliege_master_id=id,priviliege_access='tjbb').update({"priviliege_operation":request.form['tjbb']})
#			SC_Privilege.query.filter_by(priviliege_master_id=id,priviliege_access='kh').update({"priviliege_operation":request.form['kh']})
#			SC_Privilege.query.filter_by(priviliege_master_id=id,priviliege_access='dkgjztfl').update({"priviliege_operation":request.form['dkgjztfl']})
#			SC_Privilege.query.filter_by(priviliege_master_id=id,priviliege_access='xdgzlclb').update({"priviliege_operation":request.form['xdgzlclb']})
#			SC_Privilege.query.filter_by(priviliege_master_id=id,priviliege_access='pcscbbcx').update({"priviliege_operation":request.form['pcscbbcx']})
#			SC_Privilege.query.filter_by(priviliege_master_id=id,priviliege_access='zhgllbb').update({"priviliege_operation":request.form['zhgllbb']})

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
		#privileges = SC_Privilege.query.filter_by(priviliege_master_id=id).order_by(SC_Privilege.id).all()

		return render_template("System/edit_role.html",role=role)