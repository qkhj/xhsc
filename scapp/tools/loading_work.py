#coding:utf-8
from apscheduler.scheduler import Scheduler
from scapp.views.cust_mgr.autoload.load import scriptload
from daily_work import daily_work
from monthly_work import monthly_work


class timing():
    def __init__(self):
        sched = Scheduler()
        sched.daemonic = False
        script = scriptload()
        monthly = monthly_work()
        daily = daily_work()
        sched.add_cron_job(script.rise, month='4,7,10,12', day='10', hour='1')
        sched.add_cron_job(script.kpi, month='1-12', day='1', hour='2')  #每月1号凌晨2点创建当月评估表
        sched.add_cron_job(script.total, month='1-12', day='1', hour='2')  #每月1号凌晨2点创建上月余额规模
        sched.add_cron_job(script.perform, month='1-12', day='1', hour='3')  #每月1号凌晨3点初始化当月业绩表
        sched.add_cron_job(script.first, month='1-12', day='1', hour='5')  #计算历史贷款笔数分成
        sched.add_cron_job(monthly.run,month='1-12',day='1',hour='3') #银行每月客户经理有效管户更新
        sched.add_cron_job(daily.run, month='1-12',hour='4')#银行每日还款数据更新
        sched.start()