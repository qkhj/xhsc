# coding:utf-8
from flask import Module, session, request, render_template, redirect, url_for
from scapp import db
from scapp import app
from scapp.config import PER_PAGE

from scapp.models import View_Bank_Loans_Main

import datetime,time,xlwt,re
from scapp.tools.export_excel import export_excel
ezxf=xlwt.easyxf #样式转换

from scapp.models import SC_Loan_Product

# 贷款根据状态分类——6. 已发放的贷款 
@app.route('/Report/dkgjztfl_6', methods=['GET'])
def dkgjztfl_6():
	loan_product = SC_Loan_Product.query.all()
	return render_template("Report/dkgjztfl_6.html",loan_product=loan_product)

# 贷款根据状态分类——6. 已发放的贷款 
@app.route('/Report/dkgjztfl_6_search/<int:page>', methods=['POST'])
def dkgjztfl_6_search(page):
    customer_name = request.form['customer_name']
    loan_type = request.form['loan_type']
    sql = " loan_status = '6'"
    if loan_type != '0':
        sql += " and loan_type='"+loan_type+"' "
    if customer_name:
        sql += " and customer_name like '%"+customer_name+"%'"

    bank_loans_main = View_Bank_Loans_Main.query.filter(sql).paginate(page, per_page = PER_PAGE)
    return render_template("Report/dkgjztfl_6_search.html",loan_type=loan_type,customer_name=customer_name,
        bank_loans_main=bank_loans_main)

# 贷款根据状态分类——6. 已发放的贷款--导出
@app.route('/Report/dkgjztfl_6_export', methods=['POST'])
def dkgjztfl_6_export():
    customer_name = request.form['customer_name']
    loan_type = request.form['loan_type']
    sql = " loan_status = '6'"
    if loan_type != '0':
        sql += " and loan_type='"+loan_type+"' "
    if customer_name:
        sql += " and customer_name like '%"+customer_name+"%'"

    #data = View_Bank_Loans_Main.query.filter(sql)
    query_sql = "select loan_apply_id,customer_name,ratio,amount,loan_manager,'' as qishu,loan_due_date,loan_closed_date "
    query_sql += "from view_bank_loans_main where "
    query_sql += sql
    data=db.engine.execute(query_sql)

    exl_hdngs=['贷款编号','客户名称','月利率','贷款金额','负责客户经理','期数','还款截止日期','逾期截止日']

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
    filename=str(year)+'_'+str(month)+'_'+str(day)+'_'+'逾期贷款统计表'+'.xls'
    exp=export_excel()
    return exp.export_download(filename,'逾期贷款统计表',exl_hdngs,data,exl_hdngs_xf,data_xfs)

