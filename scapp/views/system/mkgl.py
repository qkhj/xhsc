# coding:utf-8
from flask import Module, session, request, render_template, redirect, url_for, flash

from scapp.models import SC_Application
from scapp.models import SC_Menu
import json
from scapp import db
from scapp import app

# 模块管理
@app.route('/System/mkgl', methods=['GET'])
def System_mkgl():
    return render_template("System/mkgl.html")

# 加载树
@app.route('/System/tree/access', methods=['GET','POST'])
def init_access_tree():
	# 加载所有
	data = []
	root_children = []
	# 根节点
	root = {}
	root['id'] = 0
	root['name'] = u'模块资源列表'
	root['type'] = 'root'
	root['open'] = 1
	#拼接根节点
	data.append(root)
	#拼接子节点
	app_tree = SC_Application.query.order_by("id").all()
	for app in app_tree:
		dic = {}
		dic['id'] = app.id
		dic['name'] = app.application_name
		dic['code'] = app.application_code
		dic['type'] = 'sc_application'
		dic['open'] = 1
		app_children = []
		menu_tree = SC_Menu.query.filter_by(application=app.id).order_by("id").all()
		for menu in menu_tree:
			app_children.append({'id':menu.id,'name':menu.menu_name,'open':1,'type':'sc_menu','code':menu.menu_code})
		dic['children'] = app_children
		root_children.append(dic)
	root['children'] = root_children
	return json.dumps(data) # 返回json

# 新增模块或菜单
@app.route('/System/new_mkgl/<pType>/<int:pId>', methods=['GET','POST'])
def new_mkgl(pType,pId):
    if request.method == 'POST':
        try:
			if pType == 'root':#当前选中根节点，添加app
				SC_Application(request.form['code'],request.form['name']).add()
			elif pType == 'sc_application':#当前选中app节点，添加menu
				SC_Menu(request.form['code'],request.form['name'],pId).add()

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

        return redirect('System/mkgl')
    else:
        return render_template("System/new_mkgl.html",pType=pType,pId=pId)

# 编辑模块或菜单
@app.route('/System/edit_mkgl/<type>/<int:id>', methods=['GET','POST'])
def edit_mkgl(type,id):
    if request.method == 'POST':
        try:
			if type == 'sc_application':
				obj = SC_Application.query.filter_by(id=id).first()
				obj.application_name = request.form['name']
				obj.application_code = request.form['code']
			elif type == 'sc_menu':
				obj = SC_Menu.query.filter_by(id=id).first()
				obj.menu_name = request.form['name']
				obj.menu_code = request.form['code']

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

        return redirect('System/mkgl')
    else:
    	if type == 'sc_application':
        	obj = SC_Application.query.filter_by(id=id).first()
        elif type == 'sc_menu':
        	obj = SC_Menu.query.filter_by(id=id).first()
        return render_template("System/edit_mkgl.html",type=type,obj=obj)
            
# 删除模块或菜单
@app.route('/System/delete_mkgl/<type>/<int:id>', methods=['GET','POST'])
def delete_mkgl(type,id):
    try:
    	if type == 'sc_application':
        	SC_Application.query.filter_by(id=id).delete()
        elif type == 'sc_menu':
        	SC_Menu.query.filter_by(id=id).delete()

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

    return redirect('System/mkgl')