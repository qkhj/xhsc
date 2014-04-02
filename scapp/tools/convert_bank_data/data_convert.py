# coding:utf-8
"""
银行每日还款数据转换主程
"""

__author__ = 'johhny'

import config
import assist
import Interface_bank_data
from db_conn import local_db_conn

logger=config.logger

s_wrong_account = set('')


def insert_update_data():
    try:
        logger.info("=======开始导入还款信息========")
        repayment_data = local_db_conn.execute(config.REPAYMENT_QUERY_STR).fetchall()
        for data in repayment_data:
            account = data['FK_LNLNS_KEY']#还款账号
            tran_no = data['LN_TNRNO_N']#期数
            repayment_day = data['LN_PPRD_RFN_DAY_N']#每期还本日
            last_repayment_day = data['LN_LST_RFN_DT_N']#实际每期最后还款日期
            crnt_pr = data['LN_CRNT_PRD_PR']#应还本金
            arfn_pr = data['LN_ARFN_PR']#已还本金
            crnt_int = data['LN_CRNT_PRD_INT']#应还利息
            arfn_int = data['LN_ARFN_INT']#已还利息

            loan_apply_id = assist.get_lai_by_account(account)
            '''
                当loan_apply_id不为空时向数据表中插入数据
            '''
            #获得需要更新的id
            update_id = Interface_bank_data.get_need_update_id()
            check_result = check_id_install(loan_apply_id, tran_no, update_id)
            if loan_apply_id is None:
                if account not in s_wrong_account:
                    Interface_bank_data.insert_wrong_account(account)
                    s_wrong_account.add(account)
                continue
            elif check_result:
                for item in update_id:
                    if loan_apply_id == item.loan_apply_id and tran_no == item.repayment_installments:
                        result = Interface_bank_data.update_rep(loan_apply_id, tran_no, last_repayment_day, crnt_pr,
                                                                arfn_pr, crnt_int, arfn_int, item.id)
            else:
                result = Interface_bank_data.insert_rep(loan_apply_id, tran_no, last_repayment_day, crnt_pr, arfn_pr,
                                                        crnt_int, arfn_int)

        logger.info("=======导入还款信息结束========")
    except():
        logger.error("error")


#判断贷款申请ID和期数是否在更新列表中
def check_id_install(loan_apply_id, tran_no, update_data):
    for item in update_data:
        if loan_apply_id == item.loan_apply_id and tran_no == item.repayment_installments:
            return True
        else:
            return False
