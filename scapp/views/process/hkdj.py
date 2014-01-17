# coding:utf-8

import os

from flask import Module, session, request, render_template, redirect, url_for,flash
from flask.ext.login import current_user
import datetime

from scapp import db
from scapp.config import logger
from scapp.config import PER_PAGE

from scapp import app

# 还款登记搜索
@app.route('/Process/hkdj/hkdj_search', methods=['GET'])
def hkdj_search():
    return render_template("Process/hkdj/hkdj_search.html")

# 还款登记
@app.route('/Process/hkdj/hkdj', methods=['GET'])
def Process_hkdj():
    return render_template("Process/hkdj/hkdj.html")
	
# 还款登记——编辑还款登记
@app.route('/Process/hkdj/edit_hkdj', methods=['GET'])
def edit_hkdj():
    return render_template("Process/hkdj/edit_hkdj.html")