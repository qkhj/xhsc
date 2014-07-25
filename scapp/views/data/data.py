# coding:utf-8

import os

from flask import Module, session, request, render_template, redirect, url_for,flash,send_from_directory,send_file
from flask.ext.login import current_user
import datetime
import urllib2 

from scapp import db
from scapp import app

# 导入本地数据-搜索
@app.route('/Data/drbdsj_search', methods=['GET'])
def drbdsj_search():
    return render_template("Data/drbdsj_search.html")    

# 导入本地数据-贷款列表 
@app.route('/Data/drbdsj', methods=['GET'])
def drbdsj():
    return render_template("Data/drbdsj.html")

# 数据同步-搜索
@app.route('/Data/sjtb_search', methods=['GET'])
def sjtb_search():
    return render_template("Data/sjtb_search.html")  
    
# 数据同步-列表
@app.route('/Data/sjtbList', methods=['GET'])
def sjtbList():
    return render_template("Data/sjtbList.html")  

# 数据同步
@app.route('/Data/sjtb', methods=['GET'])
def sjtb():
    return render_template("Data/sjtb.html") 

# 数据同步-资产负债表
@app.route('/Data/dqdcXed_zcfzb', methods=['GET'])
def dqdcXed_zcfzb1():
    return render_template("Data/dqdcXed_zcfzb.html") 

# 数据同步-交叉检验
@app.route('/Data/dqdcXed_jcjy', methods=['GET'])
def dqdcXed_jcjy1():
    return render_template("Data/dqdcXed_jcjy.html") 

# 数据同步-交叉检验
@app.route('/Data/dqdcXed_ysqkfx', methods=['GET'])
def dqdcXed_ysqkfx1():
    return render_template("Data/dqdcXed_ysqkfx.html")     

# 数据同步-现金流分析
@app.route('/Data/dqdcXed_xjlfx', methods=['GET'])
def dqdcXed_xjlfx1():
    return render_template("Data/dqdcXed_xjlfx.html") 

# 数据同步-担保抵押调查表
@app.route('/Data/dqdcXed_dbdydcb', methods=['GET'])
def dqdcXed_dbdydcb1():
    return render_template("Data/dqdcXed_dbdydcb.html") 

# 数据同步-固定资产清单
@app.route('/Data/dqdcXed_gdzcqd', methods=['GET'])
def dqdcXed_gdzcqd1():
    return render_template("Data/dqdcXed_gdzcqd.html") 

# 数据同步-库存
@app.route('/Data/dqdcXed_kc', methods=['GET'])
def dqdcXed_kc1():
    return render_template("Data/dqdcXed_kc.html") 

# 数据同步-账款清单
@app.route('/Data/dqdcXed_zkqd', methods=['GET'])
def dqdcXed_zkqd1():
    return render_template("Data/dqdcXed_zkqd.html") 

# 数据同步-基本情况
@app.route('/Data/dqdcXed_jbqk', methods=['GET'])
def dqdcXed_jbqk1():
    return render_template("Data/dqdcXed_jbqk.html") 
    