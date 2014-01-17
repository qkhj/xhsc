#coding:utf-8
__author__ = 'Johnny'
import json
from scapp import db,app
from scapp.config import logger
from flask import request
from scapp.tools import json_encoding
from json import encoder
from scapp.models.credit_data import sc_assets_loan
# 资产负债表-银行贷款，社会集资
@app.route('/Process/dqdc/new_assets_loan', methods=['GET','POST'])
def assets_loan(loan_apply_id):
    '''
    资产负债表-银行贷款，社会集资
    '''
    if request.method == 'POST':
        result={'result':'success'}
        try:
            sc_assets_loan( request.form['loan_apply_id'],request.form['loan_type'],
                                    request.form['loan_org'],request.form['loan_amount'],request.form['loan_date'],
                                    request.form['loan_deadline'],request.form['guarantee'],request.form['banlance']
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
        data = sc_assets_loan.query.filter_by(loan_apply_id==loan_apply_id).all()
        encoder.FLOAT_REPR = lambda o: format(o, '.2f')#使float类型字段只显示两位小数
        return json.dumps(data,cls=json_encoding.DateEncoder,ensure_ascii=False)