# coding:utf-8
__author__ = 'johhny'
import os
# 引入日志模块
import logging
import logging.config

_HERE = os.path.dirname(__file__)
_DB_SQLITE_PATH = os.path.join(_HERE, 'scapp.sqlite')

# ========配置日志开始=================
_LOG_PATH=os.path.join(_HERE, 'log')
if not os.path.exists(_LOG_PATH):
    os.mkdir(_LOG_PATH)
_LOG_FILE_PATH=os.path.join(_LOG_PATH,'db_transfer.log')
logger = logging.getLogger('scapp')
hdlr = logging.FileHandler(_LOG_FILE_PATH)
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.INFO)
#====================================

_DBUSER = "root"  # 数据库用户名
_DBPASS = "root"  # 数据库用户名密码
_DBHOST = "192.168.0.250"  # 服务器
_DBPORT = '3306' #服务器端口
_DBNAME = "sc_test"  # 数据库名称


BANK_DBUSER = "root"  # 数据库用户名
BANK_DBPASS = "root"  # 数据库用户名密码
BANK_DBHOST = "localhost"  # 服务器
BANK_DBPORT = '3306' #服务器端口
BANK_DBNAME = "test_bank"  # 数据库名称

#本地数据库
SQLALCHEMY_LOCAL_DATABASE_URI = 'mysql://%s:%s@%s:%s/%s' % (_DBUSER, _DBPASS, _DBHOST, _DBPORT, _DBNAME)
#银行数据库
SQLALCHEMY_BANK_DATABASE_URI = 'mysql://%s:%s@%s:%s/%s' % (BANK_DBUSER, BANK_DBPASS, BANK_DBHOST, BANK_DBPORT, BANK_DBNAME)

#还款数据查询语句
REPAYMENT_QUERY_STR="SELECT FK_LNLNS_KEY, LN_TNRNO_N, LN_PPRD_RFN_DAY_N, LN_ARFN_PR, " \
                    "LN_LST_RFN_DT_N, LN_CRNT_PRD_PR, LN_CRNT_PRD_INT, LN_ARFN_INT, " \
                    "LN_BELONG_INSTN_COD FROM cbod_lnlnsdue " \
                    "WHERE (FK_LNLNS_KEY,LN_TNRNO_N) NOT IN " \
                    "(SELECT sc_approval_decision.loan_account,sc_repayment.repayment_installments " \
                    "FROM sc_repayment " \
                    "INNER JOIN sc_approval_decision ON sc_repayment.loan_apply_id = sc_approval_decision.loan_apply_id " \
                    "WHERE sc_repayment.status='3' )"

#银行贷款信息查询语句
BANK_LOANS_QUERY_STR="SELECT LN_LN_ACCT_NO,LN_ACCT_STS,LN_TOTL_LN_AMT_HYPO_AMT,LN_LN_BAL,LN_FRST_ALFD_DT_N,LN_DUE_DT_N,LN_CLSD_DT_N," \
                     "LN_ARFN_SCHD_PR_N,LN_ARFN_SCHD_INT_N,LN_DLAY_PR_TOTL,LN_DLAY_LN_DT_N FROM cbod_lnlnslns " \
                     "WHERE LN_LN_ACCT_NO NOT IN" \
                     "(SELECT loan_account FROM sc_bank_loans_main WHERE loan_status='5')"







