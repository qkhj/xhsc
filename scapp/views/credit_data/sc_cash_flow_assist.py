#coding:utf-8
__author__ = 'Johnny'

from scapp import db,app
from scapp.config import logger
from flask import request
import json
from json import encoder
from scapp.models.credit_data import sc_cash_flow_assist
# 新增现金流
@app.route('/Process/dqdc/new_xjl_cfa', methods=['GET','POST'])#现金流分析-其它费用信息
def new_xjl_cof(loan_apply_id,type):
    if request.method == 'POST':
        result={'result':'success'}
        try:
            sc_cash_flow_assist( request.form['loan_apply_id'],request.form['type'],request.form['assist_type'],
                                 request.form['month_1'],request.form['month_2'],
                                 request.form['month_3'],request.form['month_4'],request.form['month_5'],
                                 request.form['month_6'],request.form['month_7'],request.form['month_8'],
                                 request.form['month_9'],request.form['month_10'],
                                 request.form['month_11'],request.form['month_12'],
                                 request.form['month_0'],).add()
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
        cfa_data = sc_cash_flow_assist.query.filter_by(loan_apply_id==loan_apply_id,type==type).all()
        encoder.FLOAT_REPR = lambda o: format(o, '.2f')#使float类型字段只显示两位小数
        return json.dumps(cfa_data,ensure_ascii=False)
