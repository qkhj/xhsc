#coding:utf-8
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
_LOG_FILE_PATH=os.path.join(_LOG_PATH,'scapp.log')
logger = logging.getLogger('scapp')
hdlr = logging.FileHandler(_LOG_FILE_PATH)
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.WARNING)
#====================================

_DBUSER = "root"  # 数据库用户名
_DBPASS = "root"  # 数据库用户名密码
_DBHOST = "localhost"  # 服务器
_DBPORT = '3306' #服务器端口
_DBNAME = "sc_schema"  # 数据库名称

PER_PAGE = 10  # 每页数量
UPLOAD_FOLDER_REL = '/static/upload' #上传目录(相对路径)
UPLOAD_FOLDER_ABS = os.path.join(_HERE,'static\\upload') #上传目录(绝对路径)

APPY_FOLDER_REL = '/static/appy' #模板目录(相对路径)
APPY_FOLDER_ABS = os.path.join(_HERE,'static\\appy') #模板目录(绝对路径)
unopath = 'C:\PROGRA~1\OPENOF~1\program'
openofficepath = 'C:\PROGRA~1\OPENOF~1\program\python.exe'

PROCESS_STATUS_DKSQ = '101' #1.新申请
PROCESS_STATUS_DKSQXG = '102' #1.新申请被退回修改的
PROCESS_STATUS_DKSQSH = '201' #2.分配A、B、运营岗
PROCESS_STATUS_DKSQSH_JUJUE = '202' #2.申请被拒绝
PROCESS_STATUS_DQDC = '301' #3.已分配/待调查
PROCESS_STATUS_DQDCXG = '302' #3.已分配/待调查被退回修改的
PROCESS_STATUS_DKSP = '401' #4.已分配审贷会成员
PROCESS_STATUS_DKSP_JUJUE = '402' #4.调查被拒绝
PROCESS_STATUS_SPJY_TG = '501' #5.已审批通过
PROCESS_STATUS_SPJY_YTJTG = '502' #5.有条件通过
PROCESS_STATUS_SPJY_CXDC = '503' #5.重新调查
PROCESS_STATUS_SPJY_JUJUE = '504' #5.拒绝

PROCESS_STATUS_DKFKJH = '601' #6.设置还款计划

ROLE_LEVEL_ADMIN = 0 #admin
ROLE_LEVEL_ZG = 1 #主管 
ROLE_LEVEL_KHJL = 2 #客户经理 
ROLE_LEVEL_HTYY = 3 #后台运营

#XIAOWEIZHIHANG_JGH =  '321281000' # 小微支行机构号
#YUNYINGGANG_GH_GXJ = 'L025502' # 运营岗工号 葛旭娟
#YUNYINGGANG_GH_NWB = 'L025503' # 运营岗工号 倪文彬

class Config(object):
    SECRET_KEY = '\xb5\xc8\xfb\x18\xba\xc7*\x03\xbe\x91{\xfd\xe0L\x9f\xe3\\\xb3\xb1P\xac\xab\x061'
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///%s' % _DB_SQLITE_PATH
    BABEL_DEFAULT_TIMEZONE = 'Asia/Chongqing'

# 当前用的数据库配置 重写"SQLALCHEMY_DATABASE_URI"为mysql
class ProConfig(Config):
    # 微贷系统数据库配置
    SQLALCHEMY_DATABASE_URI = 'mysql://%s:%s@%s:%s/%s' % (_DBUSER, _DBPASS, _DBHOST, _DBPORT, _DBNAME)
    #SQLALCHEMY_DATABASE_URI = 'ibm_db_sa://%s:%s@%s:%s/%s' % (_DBUSER, _DBPASS, _DBHOST, _DBPORT, _DBNAME)

    #CRM数据库配置
    # SQLALCHEMY_BINDS = {
    #     'CRM_DB2':'ibm_db_sa://xhods:xhods@32.235.32.121:50001/xhods'
    # }
    # 如何使用
    #test = db.session.execute("select * from sc_role",bind=db.get_engine(app,bind="CRM_DB2")).fetchall()
    DEBUG = True

class DevConfig(Config):
    DEBUG = True

class TestConfig(Config):
    TESTING = True

#数据库路径--自动安装数据库使用 --johnny
SQLALCHEMY_DATABASE_URI = 'mysql://%s:%s@%s:%s/%s' % (_DBUSER, _DBPASS, _DBHOST, _DBPORT, _DBNAME)
#SQLALCHEMY_DATABASE_URI = 'ibm_db_sa://%s:%s@%s:%s/%s' % (_DBUSER, _DBPASS, _DBHOST, _DBPORT, _DBNAME)
#迁移数据路径 --johnny
SQLALCHEMY_MIGRATE_REPO = os.path.join(_HERE, 'db_repository')

