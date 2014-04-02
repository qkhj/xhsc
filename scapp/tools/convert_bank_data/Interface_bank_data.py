# coding:utf-8
"""
统一接口
"""
__author__ = 'johhny'
from repayment import DAO_repayment
from overdue import DAO_overdue

#DAO_repayment


def insert_rep(loan_apply_id, tran_no, last_repayment_day, crnt_pr, arfn_pr, crnt_int, arfn_int):
    """
    插入还款信息
    @param loan_apply_id:贷款id
    @param tran_no: 期数
    @param last_repayment_day:实际最后还款日
    @param crnt_pr: 应还本金
    @param arfn_pr: 已还本金
    @param crnt_int: 应还利息
    @param arfn_int: 已还利息
    @return:None
    """
    return DAO_repayment.insert_rep(loan_apply_id, tran_no, last_repayment_day, crnt_pr, arfn_pr, crnt_int, arfn_int)


def insert_wrong_account(account_no):
    """
    插入错误账号信息
    @param account_no: 账户号
    @return:None
    """
    return DAO_repayment.insert_wrong_account(account_no)


def get_need_update_id():
    """
    获得需要更新的账户ID
    @return:需要更新账户id列表
    """
    return DAO_repayment.get_need_update_id()


def update_rep(loan_apply_id,tran_no,last_repayment_day,crnt_pr,arfn_pr,crnt_int,arfn_int,id):
    """
    更新还款信息
    @param loan_apply_id:贷款id
    @param tran_no: 期数
    @param last_repayment_day:实际最后还款日
    @param crnt_pr: 应还本金
    @param arfn_pr: 已还本金
    @param crnt_int: 应还利息
    @param arfn_int: 已还利息
    @param id: id
    @return:None
    """
    return update_rep(loan_apply_id,tran_no,last_repayment_day,crnt_pr,arfn_pr,crnt_int,arfn_int,id)



def cal_last_month_intrest():
    """
    计算上个月利润贡献,插入sc_sta_mlm表中
    @return:None
    """
    return DAO_repayment.cal_last_month_intrest()

#DAO_overdue


def get_is_overdue(loan_apply_id,installments):
    """
    判断贷款在当前期数在目前的时间是否已逾期
    @param loan_apply_id: 贷款编号
    @param installments: 期数
    @return:False 逾期 or True 未逾期
    """
    return DAO_overdue.get_is_overdue(loan_apply_id,installments)



def update_overdue_rate():
    """
    更新当前所有人逾期率
    @return:None
    """
    return DAO_overdue.update_overdue_rate()

