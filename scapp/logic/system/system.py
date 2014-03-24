#coding:utf-8
from scapp.models import SC_Application
from scapp.models import SC_Menu
import json
from scapp.config import PER_PAGE

#获取系统所有模块和菜单
def get_all_module():
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
	return json.dumps(data) # 返回json

#获取对应主体的某一类权限
def get_privilege_by_access(privilege_master,privilege_master_id,privilege_access):
	return SC_Privilege.query.filter_by(privilege_master=privilege_master,priviliege_access=privilege_access,
			priviliege_master_id=privilege_master_id).order_by("id").all()