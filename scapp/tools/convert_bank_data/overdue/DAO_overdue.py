# coding:utf-8
"""
银行逾期数据转换辅助接口
"""
__author__ = 'johhny'

import datetime
from .. import assist
from ..config import logger
from ..db_conn import local_db_conn

#根据loan_apply_id查询当前日期判断是否逾期
def get_is_overdue(loan_apply_id,installments):
    QUERY_STR="SELECT clear_date FROM sc_repayment_plan_detail WHERE loan_apply_id='%s' " \
              "AND repayment_installments='%s'"%(loan_apply_id,installments)
    data=local_db_conn.execute(QUERY_STR).fetchall()
    if len(data)>0:
        repayment_date=data[0]['clear_date']
        now=datetime.datetime.now()
        if now>repayment_date:
            return True
        else:
            return False
    else:
        return False




