# coding:utf-8
from flask import Module, session, request, render_template, redirect, url_for

from scapp import app


# 贷款根据状态分类
@app.route('/Report/dkgjztfl', methods=['GET'])
def dkgjztfl():
    return render_template("Report/dkgjztfl.html")
	
# 贷款根据状态分类——1. 已发放的贷款 
@app.route('/Report/dkgjztfl_1', methods=['GET'])
def dkgjztfl_1():
    return render_template("Report/dkgjztfl_1.html")

# 贷款根据状态分类——2. 被拒绝的贷款
@app.route('/Report/dkgjztfl_2', methods=['GET'])
def dkgjztfl_2():
    return render_template("Report/dkgjztfl_2.html")

# 贷款根据状态分类——3. 贷后变更的贷款
@app.route('/Report/dkgjztfl_3', methods=['GET'])
def dkgjztfl_3():
    return render_template("Report/dkgjztfl_3.html")

# 贷款根据状态分类——4. 到期终止的贷款
@app.route('/Report/dkgjztfl_4', methods=['GET'])
def dkgjztfl_4():
    return render_template("Report/dkgjztfl_4.html")

# 贷款根据状态分类——5. 贷款余额
@app.route('/Report/dkgjztfl_5', methods=['GET'])
def dkgjztfl_5():
    return render_template("Report/dkgjztfl_5.html")

# 贷款根据状态分类——6. 逾期贷款
@app.route('/Report/dkgjztfl_6', methods=['GET'])
def dkgjztfl_6():
    return render_template("Report/dkgjztfl_6.html")

# 贷款根据状态分类——7. 预期的还款
@app.route('/Report/dkgjztfl_7', methods=['GET'])
def dkgjztfl_7():
    return render_template("Report/dkgjztfl_7.html")

# 贷款根据状态分类——8. 还贷款记录
@app.route('/Report/dkgjztfl_8', methods=['GET'])
def dkgjztfl_8():
    return render_template("Report/dkgjztfl_8.html")

