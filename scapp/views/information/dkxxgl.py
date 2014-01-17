# coding:utf-8
from flask import Module, session, request, render_template, redirect, url_for

from scapp import app

# 贷款信息管理
@app.route('/Information/dkxxgl', methods=['GET'])
def dkxxgl():
    return render_template("Information/dkxxgl.html")
	
# 贷款信息管理——贷款信息
@app.route('/Information/dkxx', methods=['GET'])
def dkxx():
    return render_template("Information/dkxx.html")

# 贷款信息管理——贷款信息(还款记录)
@app.route('/Information/dkxx_hkjl', methods=['GET'])
def dkxx_hkjl():
    return render_template("Information/dkxx_hkjl.html")

# 贷款信息管理——贷款信息(还款记录明细)
@app.route('/Information/dkxx_hkjlInfo', methods=['GET'])
def dkxx_hkjlInfo():
    return render_template("Information/dkxx_hkjlInfo.html")

# 贷款信息管理——贷款信息(贷后变更)
@app.route('/Information/dkxx_dhbg', methods=['GET'])
def dkxx_dhbg():
    return render_template("Information/dkxx_dhbg.html")

# 贷款信息管理——贷款信息(贷后变更——修改还款计划)
@app.route('/Information/dkxx_dhbg_xghkjh', methods=['GET'])
def dkxx_dhbg_xghkjh():
    return render_template("Information/dkxx_dhbg_xghkjh.html")

# 贷款信息管理——贷款信息(贷后变更——修改担保人)
@app.route('/Information/dkxx_dhbg_xgdbrsj', methods=['GET'])
def dkxx_dhbg_xgdbrsj():
    return render_template("Information/dkxx_dhbg_xgdbrsj.html")

# 贷款信息管理——贷款信息(贷后变更——修改共同借款人)
@app.route('/Information/dkxx_dhbg_xggtjkr', methods=['GET'])
def dkxx_dhbg_xggtjkr():
    return render_template("Information/dkxx_dhbg_xggtjkr.html")

# 贷款信息管理——贷款信息(贷后变更——修改抵质押信息)
@app.route('/Information/dkxx_dhbg_xgdzyxx', methods=['GET'])
def dkxx_dhbg_xgdzyxx():
    return render_template("Information/dkxx_dhbg_xgdzyxx.html")