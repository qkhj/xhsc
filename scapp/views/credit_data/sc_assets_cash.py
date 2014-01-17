#coding:utf-8
__author__ = 'Johnny'

from scapp import db,app
from scapp.config import logger
from flask import request
import json
from json import encoder
from scapp.models.credit_data import sc_assets_cash
# 新增资产负债表现金现金
@app.route('/Process/dqdc/new_assets_cash', methods=['GET','POST'])
def assets_cash(loan_apply_id):
    if request.method == 'POST':
        result={'result':'success'}
        try:
            sc_assets_cash( request.form['loan_apply_id'],request.form['see_cash'],
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
            #return redirect('/Process/dqdc/new_xjlfx')
    else :
        data = sc_assets_cash.query.filter_by(loan_apply_id==loan_apply_id).first()
        encoder.FLOAT_REPR = lambda o: format(o, '.2f')#使float类型字段只显示两位小数
        return json.dumps(data,ensure_ascii=False)