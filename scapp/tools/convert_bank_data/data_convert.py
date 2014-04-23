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
s_info_wrong_account = set('')

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
            INSERT_FLAG=True
            if loan_apply_id is None:
                if account not in s_wrong_account:
                    Interface_bank_data.insert_wrong_account(account)
                    s_wrong_account.add(account)
                continue
            elif len(update_id)>0:
                for item in update_id:
                    if loan_apply_id == item.loan_apply_id and tran_no == item.repayment_installments:
                        INSERT_FLAG=False
                        result = Interface_bank_data.update_rep(loan_apply_id, tran_no, last_repayment_day, crnt_pr,
                                                                arfn_pr, crnt_int, arfn_int, item.id)
            if INSERT_FLAG:
                result = Interface_bank_data.insert_rep(loan_apply_id, tran_no, last_repayment_day, crnt_pr, arfn_pr,
                                                        crnt_int, arfn_int)

        logger.info("=======导入还款信息结束========")

        logger.info("=======开始导入银行贷款信息========")
        bank_loans_data = local_db_conn.execute(config.BANK_LOANS_QUERY_STR).fetchall()
        for data in bank_loans_data:
            loan_account=data['LN_LN_ACCT_NO']#还款账号
            loan_apply_id = assist.get_lai_by_account(loan_account)
            loan_status=data['LN_ACCT_STS']#贷款状态
            loan_total_amount=data['LN_TOTL_LN_AMT_HYPO_AMT']#贷款总额
            loan_balance=data['LN_LN_BAL']#贷款余额
            loan_deliver_date=data['LN_FRST_ALFD_DT_N']#放款日期
            loan_due_date=data['LN_DUE_DT_N']#贷款到期日期
            loan_closed_date=data['LN_CLSD_DT_N']#贷款结清日期，未结清为0
            loan_cleared_pr_n=data['LN_ARFN_SCHD_PR_N']#已还本金期数
            loan_cleared_in_n=data['LN_ARFN_SCHD_INT_N']#已还利息期数
            loan_overdue_amount=data['LN_DLAY_PR_TOTL']#逾期金额
            loan_overdue_date=data['LN_DLAY_LN_DT_N']#逾期日期

            BANK_LOAN_UPDATE_ID=Interface_bank_data.get_need_update_bli()
            INSERT_INFO_FLAG=True

            if loan_apply_id is None:
                if loan_account not in s_info_wrong_account:
                    Interface_bank_data.insert_wrong_account(loan_account)
                    s_info_wrong_account.add(loan_account)
                continue
            elif len(BANK_LOAN_UPDATE_ID)>0:
                for obj in BANK_LOAN_UPDATE_ID:
                    if loan_apply_id == obj.loan_apply_id:
                        INSERT_INFO_FLAG=False
                        BLI_result=Interface_bank_data.update_bank_loans_info(obj['id'],loan_apply_id,loan_account,
                                    loan_status,loan_total_amount,loan_balance,loan_deliver_date,loan_due_date,
                                    loan_closed_date,loan_cleared_pr_n,loan_cleared_in_n,loan_overdue_amount,loan_overdue_date)

            if INSERT_INFO_FLAG:
                BLI_result=Interface_bank_data.insert_bank_loans_info(loan_apply_id,loan_account,
                            loan_status,loan_total_amount,loan_balance,loan_deliver_date,loan_due_date,
                            loan_closed_date,loan_cleared_pr_n,loan_cleared_in_n,loan_overdue_amount,loan_overdue_date)

        logger.info("=======导入银行贷款信息结束========")
    except():
        logger.error("error")

    Interface_bank_data.update_valid_num()
    Interface_bank_data.update_overdue_rate()

