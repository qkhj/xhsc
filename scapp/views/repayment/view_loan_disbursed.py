#coding:utf-8
__author__ = 'Johnny'

from scapp import db,app
from flask import request
from scapp.tools import json_encoding
import json,xlwt,datetime
from scapp.tools.export_excel import export_excel
ezxf=xlwt.easyxf #样式转换
# 贷款发放统计视图查询
@app.route('/repayment/loan_disbursed', methods=['GET','POST'])
def get_loan_disbursed():
    if request.method == 'GET':
        data = db.engine.execute("select * from view_loan_disbursed")
        return json.dumps(data,cls=json_encoding.DateDecimalEncoder,ensure_ascii=False)
    
@app.route('/repayment/loan_disbursed_download_all',methods=['GET'])
def download_loan_disbursed():
    data=db.engine.execute("select * from view_loan_disbursed")
    exl_hdngs=['贷款编号','客户名称','贷款金额','年利率','放款日期','贷款状态','负责客户经理']
    types=     'int         text     price    ratio    date      text        text'.split()
    exl_hdngs_xf=ezxf('font: bold on;align: wrap on,vert centre,horiz center')
    types_to_xf_map={
        'int':ezxf(num_format_str='#,##0'),
        'date':ezxf(num_format_str='yyyy-mm-dd'),
        'ratio':ezxf(num_format_str='#,##0.00%'),
        'text':ezxf(),
        'price':ezxf(num_format_str='￥#,##0.00')
    }
    data_xfs=[types_to_xf_map[t] for t in types]
    #码值转换
    for row in data:
        if row['loan_status']=='11':
            row['loan_status']='贷款期'
        elif row['loan_status']=='12':
            row['loan_status']='结清'
        elif row['loan_status']=='13':
            row['loan_status']='注销'

    date=datetime.datetime.now()
    year=date.year
    month=date.month
    day=date.day
    filename=str(year)+'_'+str(month)+'_'+str(day)+'_'+'已发放贷款统计表'+'.xls'
    exp=export_excel()
    return exp.export_download(filename,'已发放贷款统计表',exl_hdngs,data,exl_hdngs_xf,data_xfs)