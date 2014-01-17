# coding:utf-8

import os

from flask import Module, session, request, render_template, redirect, url_for,flash
from flask.ext.login import current_user
import datetime

from scapp import db
from scapp.config import logger
from scapp.config import PER_PAGE

from scapp import app

# 资产分类审核搜索
@app.route('/Process/zcflsh/zcflsh_search', methods=['GET'])
def zcflsh_search():
    return render_template("Process/zcflsh/zcflsh_search.html")

# 资产分类审核
@app.route('/Process/zcflsh/zcflsh', methods=['GET'])
def Process_zcflsh():
    return render_template("Process/zcflsh/zcflsh.html")
	
# 资产分类审核——审核资产分类
@app.route('/Process/zcflsh/check_zcfl', methods=['GET'])
def check_zcfl():
    return render_template("Process/zcflsh/check_zcfl.html")