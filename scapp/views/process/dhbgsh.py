# coding:utf-8

import os

from flask import Module, session, request, render_template, redirect, url_for,flash
from flask.ext.login import current_user
import datetime

from scapp import db
from scapp.config import logger
from scapp.config import PER_PAGE

from scapp import app

# 贷后变更审核搜索
@app.route('/Process/dhbgsh/dhbgsh_search', methods=['GET'])
def dhbgsh_search():
    return render_template("Process/dhbgsh/dhbgsh_search.html")

# 贷后变更审核
@app.route('/Process/dhbgsh/dhbgsh', methods=['GET'])
def Process_dhbgsh():
    return render_template("Process/dhbgsh/dhbgsh.html")
	
# 贷后变更审核——审核还款计划
@app.route('/Process/dhbgsh/check_hkjh', methods=['GET'])
def check_hkjh():
    return render_template("Process/dhbgsh/check_hkjh.html")

# 贷后变更审核——审核担保人数据
@app.route('/Process/dhbgsh/check_dbrsj', methods=['GET'])
def check_dbrsj():
    return render_template("Process/dhbgsh/check_dbrsj.html")

# 贷后变更审核——审核共同借款人数据
@app.route('/Process/dhbgsh/check_gtjkrsj', methods=['GET'])
def check_gtjkrsj():
    return render_template("Process/dhbgsh/check_gtjkrsj.html")

# 贷后变更审核——审核抵质押物数据
@app.route('/Process/dhbgsh/check_dzywsj', methods=['GET'])
def check_dzywsj():
    return render_template("Process/dhbgsh/check_dzywsj.html")