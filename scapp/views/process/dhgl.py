# coding:utf-8

import os

from flask import Module, session, request, render_template, redirect, url_for,flash
from flask.ext.login import current_user
import datetime

from scapp import db
from scapp.config import logger
from scapp.config import PER_PAGE

from scapp import app

# 贷后管理搜索
@app.route('/Process/dhgl/dhgl_search', methods=['GET'])
def dhgl_search():
    return render_template("Process/dhgl/dhgl_search.html")

# 贷后管理
@app.route('/Process/dhgl/dhgl', methods=['GET'])
def Process_dhgl():
    return render_template("Process/dhgl/dhgl.html")
	
# 贷后管理——贷后管理
@app.route('/Process/dhgl/edit_dhgl', methods=['GET'])
def edit_dhgl():
    return render_template("Process/dhgl/edit_dhgl.html")

# 贷后管理——新增标准
@app.route('/Process/dhgl/new_bz', methods=['GET'])
def new_bz():
    return render_template("Process/dhgl/new_bz.html")

# 贷后管理——新增非标准
@app.route('/Process/dhgl/new_fbz', methods=['GET'])
def new_fbz():
    return render_template("Process/dhgl/new_fbz.html")
        
# 贷后管理——管理信息列表
@app.route('/Process/dhgl/glxxlb', methods=['GET'])
def dhgl_glxxlb():
    return render_template("Process/dhgl/glxxlb.html")

# 贷后管理——管理信息
@app.route('/Process/dhgl/glxx', methods=['GET'])
def dhgl_glxx():
    return render_template("Process/dhgl/glxx.html")

# 贷后管理——非标监控说明
@app.route('/Process/dhgl/fbjksm', methods=['GET'])
def dhgl_fbjksm():
    return render_template("Process/dhgl/fbjksm.html")