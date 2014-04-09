# coding:utf-8
from flask import Module, session, request, render_template, redirect, url_for
from scapp import db
from scapp import app
from scapp.config import PER_PAGE
from scapp.config import PROCESS_STATUS_DKFKJH

from scapp.models import View_Loan_Disbursed

import datetime,time,xlwt,re
from scapp.tools.export_excel import export_excel
ezxf=xlwt.easyxf #样式转换

# 贷款根据状态分类
@app.route('/Report/dkgjztfl', methods=['GET'])
def dkgjztfl():
    return render_template("Report/dkgjztfl.html")
	
# 贷款根据状态分类——1. 已发放的贷款 
@app.route('/Report/dkgjztfl_1', methods=['GET'])
def dkgjztfl_1():
    return render_template("Report/dkgjztfl_1.html")

# 贷款根据状态分类——1. 已发放的贷款 
@app.route('/Report/dkgjztfl_1_search/<int:page>', methods=['POST'])
def dkgjztfl_1_search(page):
    customer_name = request.form['customer_name']
    loan_type = request.form['loan_type']
    sql = ""
    if loan_type != '0':
        sql = "loan_type='"+loan_type+"' and "
    sql += " loan_status='"+PROCESS_STATUS_DKFKJH+"'"
    if customer_name:
        sql += " and customer_name like '%"+customer_name+"%'"

    view_loan_disbursed = View_Loan_Disbursed.query.filter(sql).paginate(page, per_page = PER_PAGE)
    return render_template("Report/dkgjztfl_1_search.html",loan_type=loan_type,customer_name=customer_name,
        view_loan_disbursed=view_loan_disbursed)

# 贷款根据状态分类——1. 已发放的贷款--导出
@app.route('/Report/dkgjztfl_1_export', methods=['POST'])
def dkgjztfl_1_export():
    customer_name = request.form['customer_name']
    loan_type = request.form['loan_type']
    sql = ""
    if loan_type != '0':
        sql = "loan_type='"+loan_type+"' and "
    sql += " loan_status='"+PROCESS_STATUS_DKFKJH+"'"
    if customer_name:
        sql += " and customer_name like '%"+customer_name+"%'"

    data = View_Loan_Disbursed.query.filter(sql)

    exl_hdngs=['贷款编号','客户名称','利率','放款日期','贷款金额','负责客户经理','贷款状态']

    type_str = 'text text text date text text text'#1
    types= type_str.split()

    exl_hdngs_xf=ezxf('font: bold on;align: wrap on,vert centre,horiz center')
    types_to_xf_map={
        'int':ezxf(num_format_str='#,##0'),
        'date':ezxf(num_format_str='yyyy-mm-dd'),
        'datetime':ezxf(num_format_str='yyyy-mm-dd HH:MM:SS'),
        'ratio':ezxf(num_format_str='#,##0.00%'),
        'text':ezxf(),
        'price':ezxf(num_format_str='￥#,##0.00')
    }

    data_xfs=[types_to_xf_map[t] for t in types]
    date=datetime.datetime.now()
    year=date.year
    month=date.month
    day=date.day
    filename=str(year)+'_'+str(month)+'_'+str(day)+'_'+'已发放的贷款统计表'+'.xls'
    exp=export_excel()
    return exp.export_download(filename,'已发放的贷款统计表',exl_hdngs,data,exl_hdngs_xf,data_xfs)

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

