#coding:utf-8
from scapp import db
import json
import datetime

from flask.ext.login import current_user

# 用户、角色 关联表
class SC_UserRole(db.Model):
    __tablename__ = 'sc_userrole' 
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('sc_user.id'))
    role_id = db.Column(db.Integer, db.ForeignKey('sc_role.id'))
    create_user = db.Column(db.Integer)
    create_date = db.Column(db.DateTime)
    modify_user = db.Column(db.Integer)
    modify_date = db.Column(db.DateTime)

    #外键
    role = db.relationship('SC_Role', backref='role')
    #外键
    user = db.relationship('SC_User', backref='user')

    def __init__(self,user_id,role_id):
        self.user_id = user_id
        self.role_id = role_id
        self.create_user = current_user.id
        self.create_date = datetime.datetime.now()
        self.modify_user = current_user.id
        self.modify_date = datetime.datetime.now()

    def add(self):
        db.session.add(self)

# 用户表
class SC_User(db.Model):
    __tablename__ = 'sc_user' 
    id = db.Column(db.Integer, primary_key=True)
    login_name = db.Column(db.String(16))
    login_password = db.Column(db.String(16))
    real_name = db.Column(db.String(32))
    sex = db.Column(db.String(1))
    mobile = db.Column(db.String(16))
    department = db.Column(db.Integer, db.ForeignKey('sc_org.id'))
    level = db.Column(db.Integer) # 审批级别(数字标识)
    active = db.Column(db.String(1))
    is_leader = db.Column(db.String(1)) # 是否是组长
    belong_leader = db.Column(db.Integer) # 所属组长
    create_user = db.Column(db.Integer)
    create_date = db.Column(db.DateTime)
    modify_user = db.Column(db.Integer)
    modify_date = db.Column(db.DateTime)

    #外键
    org = db.relationship('SC_Org', backref='org')

    def __init__(self,login_name,login_password,real_name,sex,mobile,department,level,active,is_leader,belong_leader):
        self.login_name = login_name
        self.login_password = login_password
        self.real_name = real_name
        self.sex = sex
        self.mobile = mobile
        self.department = department
        self.level = level
        self.active = active
        self.is_leader = is_leader
        self.belong_leader = belong_leader
        self.create_user = current_user.id
        self.create_date = datetime.datetime.now()
        self.modify_user = current_user.id
        self.modify_date = datetime.datetime.now()

    def add(self):
        db.session.add(self)

    # flask-login 需要的4个函数---start
    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)
    # flask-login 需要的4个函数---end

# 角色表
class SC_Role(db.Model):
    __tablename__ = 'sc_role' 
    id = db.Column(db.Integer, primary_key=True)
    role_name = db.Column(db.String(16))
    role_level = db.Column(db.Integer)

    create_user = db.Column(db.Integer)
    create_date = db.Column(db.DateTime)
    modify_user = db.Column(db.Integer)
    modify_date = db.Column(db.DateTime)

    def __init__(self, role_name, role_level):
        self.role_name = role_name
        self.role_level = role_level
        self.create_user = current_user.id
        self.create_date = datetime.datetime.now()
        self.modify_user = current_user.id
        self.modify_date = datetime.datetime.now()

    def add(self):
        db.session.add(self)

# 权限表
class SC_Privilege(db.Model):
    __tablename__ = 'sc_privilege' 
    id = db.Column(db.Integer, primary_key=True)
    privilege_master = db.Column(db.String(32))
    priviliege_master_id = db.Column(db.Integer)
    priviliege_access = db.Column(db.String(32))
    priviliege_access_value = db.Column(db.String(32))
    priviliege_operation = db.Column(db.Integer)

    def __init__(self,privilege_master,priviliege_master_id, priviliege_access,priviliege_access_value,priviliege_operation):
        self.privilege_master = privilege_master
        self.priviliege_master_id = priviliege_master_id
        self.priviliege_access = priviliege_access
        self.priviliege_access_value = priviliege_access_value
        self.priviliege_operation = priviliege_operation

    def add(self):
        db.session.add(self)

# 模块表
class SC_Application(db.Model):
    __tablename__ = 'sc_application' 
    id = db.Column(db.Integer, primary_key=True)
    application_code = db.Column(db.String(32))
    application_name = db.Column(db.String(32))
    application_desc = db.Column(db.Integer)

    def __init__(self, application_code, application_name):
        self.application_code = application_code
        self.application_name = application_name

    def add(self):
        db.session.add(self)

# 菜单表
class SC_Menu(db.Model):
    __tablename__ = 'sc_menu' 
    id = db.Column(db.Integer, primary_key=True)
    menu_code = db.Column(db.String(32))
    menu_name = db.Column(db.String(32))
    menu_desc = db.Column(db.Integer)
    application = db.Column(db.Integer, db.ForeignKey('sc_application.id'))

    #外键
    application_fk = db.relationship('SC_Application', backref='application_fk')

    def __init__(self, menu_code,menu_name,application):
        self.menu_code = menu_code
        self.menu_name = menu_name
        self.application = application

    def add(self):
        db.session.add(self)

# 机构表
class SC_Org(db.Model):
    __tablename__ = 'sc_org' 
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32))
    level = db.Column(db.Integer)
    pId = db.Column(db.Integer)
    open = db.Column(db.Boolean)

    def __init__(self, name,level, pId):
        self.name = name
        self.level = level
        self.pId = pId
        self.open = True

    def add(self):
        db.session.add(self)