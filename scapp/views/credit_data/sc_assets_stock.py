#coding:utf-8
__author__ = 'Johnny'
import json
from scapp import db,app
from scapp.config import logger
from flask import request
from scapp.tools import json_encoding
from json import encoder
from scapp.models.credit_data import sc_assets_stock
# 资产负债表-存货
@app.route('/Process/dqdc/new_assets_stock', methods=['GET','POST'])
def assets_stock(loan_apply_id):
    '''
    资产负债表-存货
    '''
    if request.method == 'POST':
        result={'result':'success'}
        try:
            sc_assets_stock( request.form['loan_apply_id'],request.form['stock_type'],
                            request.form['stock_evaluate'],request.form['stock_mobility'],request.form['proportion'],
                            request.form['amount']
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
        data = sc_assets_stock.query.filter_by(loan_apply_id==loan_apply_id).all()
        encoder.FLOAT_REPR = lambda o: format(o, '.2f')#使float类型字段只显示两位小数
        return json.dumps(data,ensure_ascii=False)