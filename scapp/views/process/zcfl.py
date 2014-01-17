# coding:utf-8

import os

from flask import Module, session, request, render_template, redirect, url_for,flash
from flask.ext.login import current_user
import datetime

from scapp import db
from scapp.config import logger
from scapp.config import PER_PAGE

from scapp import app

# 资产分类搜索
@app.route('/Process/zcfl/zcfl_search', methods=['GET'])
def zcfl_search():
    return render_template("Process/zcfl/zcfl_search.html")

# 资产分类
@app.route('/Process/zcfl/zcfl', methods=['GET'])
def Process_zcfl():
    return render_template("Process/zcfl/zcfl.html")
	
# 资产分类——编辑资产分类
@app.route('/Process/zcfl/edit_zcfl', methods=['GET'])
def edit_zcfl():
    return render_template("Process/zcfl/edit_zcfl.html")