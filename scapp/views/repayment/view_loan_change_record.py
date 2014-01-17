# coding:utf-8
__author__ = 'johhny'

from scapp import app,db
import json
from scapp.tools import json_encoding
from scapp.config import PER_PAGE

from flask import render_template,request


#显示贷后变更
@app.route('/repayment/dhbg',methods=['GET'])
def get_dhbg():
    data=db.engine.execute("select * from view_loan_change_record").fetchall()
    return render_template('/Process/dhbg/dhbg.html',data=data)

#条件查找贷后变更
@app.route('/repayment/dhbg/search',methods=['GET','POST'])
def get_change_record():
    if request.method=='GET':
        page=int(request.args.get('page',1))
        loan_apply_id =request.args.get('loan_apply_id',None)
        customer_name=request.args.get('customer_name',None)
        loan_manager=request.args.get('loan_manager',None)
        where_condition=' WHERE 1=1 '
        if not loan_apply_id :
            where_condition+='AND loan_apply_id='+loan_apply_id+''
        elif not customer_name :
            where_condition+='AND customer_name='+customer_name+''
        elif not loan_manager :
            where_condition+='AND loan_manager'+loan_manager+''

        data=db.engine.execute("select * from view_query_loan"+where_condition).fetchall()

        start_num=(int(page)-1)*PER_PAGE
        end_num=int(page)*PER_PAGE

        result=data[start_num:end_num]

        return render_template('/Process/dhbg/dhbg.html',result=result)


