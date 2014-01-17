# coding:utf-8

import os

from flask import Module, session, request, render_template, redirect, url_for,flash
from flask.ext.login import current_user
import datetime

from scapp import db
from scapp.config import logger
from scapp.config import PER_PAGE

from scapp import app

# 贷后变更搜索
@app.route('/Process/dhbg/dhbg_search', methods=['GET'])
def dhbg_search():
    return render_template("Process/dhbg/dhbg_search.html")

# 贷后变更
@app.route('/Process/dhbg/dhbg', methods=['GET'])
def Process_dhbg():
    return render_template("Process/dhbg/dhbg.html")
	
# 贷后变更——编辑贷后变更
@app.route('/Process/dhbg/edit_dhbg', methods=['GET'])
def edit_dhbg():
    return render_template("Process/dhbg/edit_dhbg.html")

# 贷后变更——编辑贷后变更(基础信息)
@app.route('/Process/dhbg/jcxx', methods=['GET'])
def dhbg_jcxx():
    return render_template("Process/dhbg/jcxx.html")

# 贷后变更——编辑贷后变更(修改还款计划)
@app.route('/Process/dhbg/edit_hkjh', methods=['GET'])
def edit_hkjh():
    return render_template("Process/dhbg/edit_hkjh.html")

# 贷后变更——编辑贷后变更(修改担保人数据)
@app.route('/Process/dhbg/edit_dbrsj', methods=['GET'])
def edit_dbrsj():
    return render_template("Process/dhbg/edit_dbrsj.html")

# 贷后变更——编辑贷后变更(修改共同借款人数据)
@app.route('/Process/dhbg/edit_gtjkrsj', methods=['GET'])
def edit_gtjkrsj():
    return render_template("Process/dhbg/edit_gtjkrsj.html")

# 贷后变更——编辑贷后变更(修改抵质押物数据)
@app.route('/Process/dhbg/edit_dzywsj', methods=['GET'])
def edit_dzywsj():
    return render_template("Process/dhbg/edit_dzywsj.html")