#coding:utf-8
__author__ = 'Johnny'
import json
from scapp import db,app
from scapp.config import logger
from flask import request
from scapp.tools import json_encoding
from json import encoder
from scapp.models.credit_data import sc_assets_receipts
# 资产负债表-预收账款
@app.route('/Process/dqdc/new_assets_receipts', methods=['GET','POST'])
def assets_receipts(loan_apply_id):
    '''
    资产负债表-预收账款
    '''
    if request.method == 'POST':
        result={'result':'success'}
        try:
            sc_assets_receipts( request.form['loan_apply_id'],request.form['source'],
                            request.form['occur_date'],request.form['describe'],request.form['amount']
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
    else :
        data = sc_assets_receipts.query.filter_by(loan_apply_id==loan_apply_id).all()
        encoder.FLOAT_REPR = lambda o: format(o, '.2f')#使float类型字段只显示两位小数
        return json.dumps(data,cls=json_encoding.DateEncoder,ensure_ascii=False)