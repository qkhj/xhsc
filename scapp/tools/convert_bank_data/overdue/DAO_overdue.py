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
            insert_overdue(loan_apply_id,installments)
            return False
    else:
        return False


#有逾期向客户经理每月信息统计表中插入逾期数据
def insert_overdue(loan_apply_id,installments):
    overdue_amount=get_overdue_amount(loan_apply_id,installments)
    user_id=assist.get_user_id_by_lai(loan_apply_id)
    #获取当前时间并转换为%Y-%m格式 用来与数据库中数据匹配
    now=datetime.datetime.now()
    month=datetime.datetime.strftime(now,'%Y-%m')
    UPDATE_STR="UPDATE sc_sta_mlm set overdue_amount=%s WHERE " \
                       "user_id=%s AND month=%d"%(overdue_amount,user_id,month)
    logger.info(UPDATE_STR)
    trans_local=local_db_conn.begin()
    try:
        local_db_conn.execute(UPDATE_STR)
        trans_local.commit()
    except():
        logger.error("error")
        trans_local.rollback()


#取得逾期金额
def get_overdue_amount(loan_apply_id,installments):
    QUERY_STR="SELECT (srd.total-sr.total_repayment) AS overdue_amount " \
              "FROM sc_repayment_plan_detail AS srd,sc_repayment AS sr " \
              "WHERE srd.loan_apply_id=%s AND sr.loan_apply_id=%s AND " \
              "srd.repayment_installments=%s AND sr.repayment_installments=%s"%(loan_apply_id,loan_apply_id,installments,installments)
    return local_db_conn.execute(QUERY_STR).fetchall()[0]['overdue_amount']


#每日统计当前所有人逾期比率
def update_overdue_rate():
    #获取所有已逾期的贷款编号
    QUERY_STR_OD="SELECT COUNT(*) AS overdue,sla.A_loan_officer,sr.repayment_isntallments FROM sc_repayment AS sr INNER JOIN sc_loan_apply AS sla " \
                  "ON sr.loan_apply_id=sla.id WHERE sr.status='2'"
    data_OD=local_db_conn.execute(QUERY_STR_OD).fetchall()
    if len(data_OD)>0:
        for obj in data_OD:
            #计算逾期率
            hold_amount=get_hold_amount_by_id(obj['A_loan_officer'])
            overdue_rate=obj['overdue']/hold_amount
            #获取当前时间并转换为%Y-%m格式 用来与数据库中数据匹配
            now=datetime.datetime.now()
            month=datetime.datetime.strftime(now,'%Y-%m')
            UPDATE_STR="UPDATE sc_sta_mlm set overdue_rate=%s WHERE " \
                       "user_id=%s AND month=%d"%(overdue_rate,obj['A_loan_officer'],month)
            logger.info(UPDATE_STR)
            trans_local=local_db_conn.begin()
            try:
                local_db_conn.execute(UPDATE_STR)
                trans_local.commit()
            except():
                logger.error("error")
                trans_local.rollback()

#获得用户当前所拥有的所有管户数
def get_hold_amount_by_id(user_id):
    QUERY_STR="SELECT valid_sum,month FROM sc_performance_list WHERE manager_id=%s " \
              "AND date_format(month,'%Y-%m')=date_format(now(),'%Y-%m')"%(user_id)
    return local_db_conn.execute(QUERY_STR).fetchall()[0]['valid_sum']


