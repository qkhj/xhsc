#coding:utf-8
__author__ = 'Johnny'

from scapp import db,app
from scapp.config import logger
from flask import request, flash
from scapp.tools import json_encoding
import json
from scapp.models.credit_data import sc_assets_acceptances
# 新增承兑汇票
@app.route('/Process/dqdc/new_assets_aa', methods=['GET','POST'])
def new_assets_aa(loan_apply_id):
    if request.method == 'POST':
        result={'result':'success'}
        try:
            sc_assets_acceptances( request.form['loan_apply_id'],request.form['bank'],
                                   request.form['account_expiry_date'],request.form['account_balance']
            ).add()
            # 事务提交
            db.session.commit()
            # 消息闪现
            #flash('保存成功','Success')
        except:
            # 回滚
            db.session.rollback()
            logger.exception('exception')
            # 消息闪现
            #flash('保存失败','Error')
            result={'result':'fail'}
        finally:
            return json.dumps(result,ensure_ascii=False)
        #return redirect('/Process/dqdc/new_xjlfx')
    else :
        cfa_data = sc_assets_acceptances.query.filter_by(loan_apply_id==loan_apply_id).all()
        return json.dumps(cfa_data,cls=json_encoding.DateEncoder,ensure_ascii=False)