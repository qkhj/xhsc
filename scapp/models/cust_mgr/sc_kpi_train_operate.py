# coding:utf-8
from scapp import db
from flask.ext.login import current_user

#培训期课堂纪律考核表
class SC_Kpi_Train_Operate(db.Model):
    __tablename__ = 'sc_kpi_train_operate'
    id = db.Column(db.Integer, primary_key=True)
    job_tendency = db.Column(db.String(255))
    index = db.Column(db.Integer)#序号(第几次评估)
    assess_date = db.Column(db.Date)#评估时间',
    marketing_plain = db.Column(db.String(4))
    marketing_complete = db.Column(db.String(4))
    marketing_score = db.Column(db.String(4))
    sign_plain = db.Column(db.String(4))
    sign_complete = db.Column(db.String(4))
    sign_score = db.Column(db.String(4))
    loan_balance_plain = db.Column(db.String(32))
    loan_balance_complete = db.Column(db.String(32))
    loan_balance_score = db.Column(db.String(4))
    monitor_plain = db.Column(db.String(4))
    monitor_complete = db.Column(db.String(4))
    monitor_score = db.Column(db.String(4))
    ywdlx = db.Column(db.String(4))
    yxnl = db.Column(db.String(4))
    dqdc = db.Column(db.String(4))
    sdhcs = db.Column(db.String(4))
    jszs = db.Column(db.String(4))
    khfw = db.Column(db.String(4))
    kqjl = db.Column(db.String(4))
    zrx = db.Column(db.String(4))
    gtxt = db.Column(db.String(4))
    tdxz = db.Column(db.String(4))
    total = db.Column(db.String(4))#综合得分',
    result = db.Column(db.Integer)#评估结果(1 优秀 2 良好 3 及格 4 不及格)',
    performance = db.Column(db.String(255))#综合表现',
    focus_on = db.Column(db.String(255))#重点关注',
    next_work_target = db.Column(db.String(255))#下棋工作指标',
    individual_expectations = db.Column(db.String(255))#个人期望',
    user_id = db.Column(db.Integer)
    date_1 = db.Column(db.Date)
    manager = db.Column(db.Integer)
    date_2 = db.Column(db.Date)
    bank_director = db.Column(db.Integer)
    date_3 = db.Column(db.Date)

    def __init__(self, job_tendency, index, assess_date, marketing_plain,
                 marketing_complete, marketing_score, sign_plain, sign_complete, sign_score, loan_balance_plain,
                 loan_balance_complete,
                 loan_balance_score, monitor_plain, monitor_complete, monitor_score, ywdlx, yxnl, dqdc, sdhcs, jszs,
                 khfw, kqjl,
                 zrx, gtxt, tdxz, total, result, performance, focus_on, next_work_target, individual_expectations,
                 user_id, date_1, manager, date_2):
        self.job_tendency = job_tendency
        self.index = index
        self.assess_date = assess_date
        self.marketing_plain = marketing_plain
        self.marketing_complete = marketing_complete
        self.marketing_score = marketing_score
        self.sign_plain = sign_plain
        self.sign_complete = sign_complete
        self.sign_score = sign_score
        self.loan_balance_plain = loan_balance_plain
        self.loan_balance_complete = loan_balance_complete
        self.loan_balance_score = loan_balance_score
        self.monitor_plain = monitor_plain
        self.monitor_complete = monitor_complete
        self.monitor_score = monitor_score
        self.ywdlx = ywdlx
        self.yxnl = yxnl
        self.dqdc = dqdc
        self.sdhcs = sdhcs
        self.jszs = jszs
        self.khfw = khfw
        self.kqjl = kqjl
        self.zrx = zrx
        self.gtxt = gtxt
        self.tdxz = tdxz
        self.total = total
        self.result = result
        self.performance = performance
        self.focus_on = focus_on
        self.next_work_target = next_work_target
        self.individual_expectations = individual_expectations
        self.user_id = user_id
        self.date_1 = date_1
        self.manager = manager
        self.date_2 = date_2

    def add(self):
        db.session.add(self)