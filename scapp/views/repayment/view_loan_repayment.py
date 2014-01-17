#coding:utf-8
__author__ = 'Johnny'

from scapp import db,app
from flask import request
from scapp.tools import json_encoding
import json,xlwt,datetime
from scapp.tools.export_excel import export_excel
ezxf=xlwt.easyxf #样式转换

# 贷款还款统计视图查询
@app.route('/repayment/loan_repayment', methods=['GET','POST'])
def get_loan_repayment():
    if request.method == 'GET':
        data = db.engine.execute("select * from view_loan_repayment")
        return json.dumps(data,cls=json_encoding.DateDecimalEncoder,ensure_ascii=False)
    
@app.route('/repayment/loan_repayment_download_all',methods=['GET'])
def download_loan_repayment():
    data=db.engine.execute("select * from view_loan_repayment")
    exl_hdngs=['实际还款日期','贷款编号','客户名称','还款总额','本金','利息','期数','利率','负责客户经理']
    types=     'date         text     text        price   price   price  int   ratio    text'.split()
    exl_hdngs_xf=ezxf('font: bold on;align: wrap on,vert centre,horiz center')
    types_to_xf_map={
        'int':ezxf(num_format_str='#,##0'),
        'date':ezxf(num_format_str='yyyy-mm-dd'),
        'ratio':ezxf(num_format_str='#,##0.00%'),
        'text':ezxf(),
        'price':ezxf(num_format_str='￥#,##0.00')
    }
    data_xfs=[types_to_xf_map[t] for t in types]
    date=datetime.datetime.now()
    year=date.year
    month=date.month
    day=date.day
    filename=str(year)+'_'+str(month)+'_'+str(day)+'_'+'贷款还款统计表'+'.xls'
    exp=export_excel()
    return exp.export_download(filename,'贷款还款统计表',exl_hdngs,data,exl_hdngs_xf,data_xfs)