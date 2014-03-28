# coding:utf-8
from flask import Module, session, request, render_template, redirect, url_for,flash
from flask.ext.login import login_user, logout_user, current_user, login_required

from scapp.models import SC_User
from scapp.logic.cust_mgr import sc_kpi
from scapp.models.cust_mgr.sc_kpi_train import SC_Kpi_Train
from scapp.models.cust_mgr.sc_kpi_train_final import SC_Kpi_Train_Final
from scapp.models.cust_mgr.sc_kpi_train_operate import SC_Kpi_Train_Operate

from scapp import app
from scapp import db
from scapp.config import logger

import datetime

# 培训期评估——搜索
@app.route('/Performance/ygpgkh/pxqpg_search', methods=['GET'])
def pxqpg_search():
    return render_template("Performance/ygpgkh/pxqpg_search.html")

# 培训期评估列表
@app.route('/Performance/ygpgkh/pxqpglist', methods=['GET'])
def pxqpglist():
    kpi_train_final = sc_kpi.get_user_kpi_train_final()
    return render_template("Performance/ygpgkh/pxqpglist.html",kpi_train_final=kpi_train_final)

# 培训期评估(废弃)
@app.route('/Performance/ygpgkh/pxqpg', methods=['GET'])
def pxqpg():
    return render_template("Performance/ygpgkh/pxqpg.html")

# 课堂培训评估
@app.route('/Performance/ygpgkh/ktpxpg/<int:user_id>', methods=['GET','POST'])
def ktpxpg(user_id):
    if request.method == 'GET':
        user = SC_User.query.filter_by(id=user_id).first()
        kpi_train = SC_Kpi_Train.query.filter_by(user_id=user_id).first()
        return render_template("Performance/ygpgkh/ktpxpg.html",user=user,kpi_train=kpi_train)
    else:
        try:
            kpi_train = SC_Kpi_Train.query.filter_by(user_id=user_id).first()
            if kpi_train:
                kpi_train.train_date = request.form['train_date']
                kpi_train.job_tendency = request.form['job_tendency']
                kpi_train.class_hour = request.form['class_hour']
                kpi_train.cqqk_1 = request.form['cqqk_1']
                kpi_train.cqqk_2 = request.form['cqqk_2']
                kpi_train.ktjl_1 = request.form['ktjl_1']
                kpi_train.ktjl_2 = request.form['ktjl_2']
                kpi_train.ktfy_1 = request.form['ktfy_1']
                kpi_train.ktfy_2 = request.form['ktfy_2']
                kpi_train.ktcs_1 = request.form['ktcs_1']
                kpi_train.ktcs_2 = request.form['ktcs_2']
                kpi_train.mnbx_1 = request.form['mnbx_1']
                kpi_train.mnbx_2 = request.form['mnbx_2']
                kpi_train.ztbx_1 = request.form['ztbx_1']
                kpi_train.ztbx_2 = request.form['ztbx_2']
                kpi_train.jszs_1 = request.form['jszs_1']
                kpi_train.jszs_2 = request.form['jszs_2']
                kpi_train.tdxz_1 = request.form['tdxz_1']
                kpi_train.tdxz_2 = request.form['tdxz_2']
                kpi_train.xtgt_1 = request.form['xtgt_1']
                kpi_train.xtgt_2 = request.form['xtgt_2']
                kpi_train.jyks_1 = request.form['jyks_1']
                kpi_train.jyks_2 = request.form['jyks_2']
                kpi_train.total = request.form['total']
                kpi_train.result = request.form['result']
                kpi_train.performance = request.form['performance']
                kpi_train.focus_on = request.form['focus_on']
                kpi_train.next_work_target = request.form['next_work_target']
                kpi_train.individual_expectations = request.form['individual_expectations']
                kpi_train.user_id = user_id
                kpi_train.date_1 = datetime.datetime.now()
                kpi_train.manager = current_user.id
                kpi_train.date_2 = datetime.datetime.now()
            else:
                SC_Kpi_Train(request.form['train_date'],request.form['job_tendency'],request.form['class_hour'],
                    request.form['cqqk_1'],request.form['cqqk_2'],request.form['ktjl_1'],request.form['ktjl_2'],
                    request.form['ktfy_1'],request.form['ktfy_2'],request.form['ktcs_1'],request.form['ktcs_2'],
                    request.form['mnbx_1'],request.form['mnbx_2'],request.form['ztbx_1'],request.form['ztbx_2'],
                    request.form['jszs_1'],request.form['jszs_2'],request.form['tdxz_1'],request.form['tdxz_2'],
                    request.form['xtgt_1'],request.form['xtgt_2'],request.form['jyks_1'],request.form['jyks_2'],
                    request.form['total'],request.form['result'],request.form['performance'],request.form['focus_on'],
                    request.form['next_work_target'],request.form['individual_expectations'],
                    user_id,datetime.datetime.now(),current_user.id,datetime.datetime.now()).add()

            #同时修改SC_Kpi_Train_Final表
            kpi_train_final = SC_Kpi_Train_Final.query.filter_by(user_id=user_id).first()
            if kpi_train_final:
                kpi_train_final.score_1 = request.form['total']
            else:
                kpi_train_final = SC_Kpi_Train_Final(user_id)
                kpi_train_final.add()
                db.session.flush()
                kpi_train_final.score_1 = request.form['total']

            # 事务提交
            db.session.commit()
            # 消息闪现
            flash('保存成功','success')
        except:
            # 回滚
            db.session.rollback()
            logger.exception('exception')
            # 消息闪现
            flash('保存失败','error')

        return redirect('Performance/ygpgkh/pxqpglist')

# 实际操作评估
@app.route('/Performance/ygpgkh/sjczpg/<int:index>/<int:user_id>', methods=['GET','POST'])
def sjczpg(index,user_id):
    if request.method == 'GET':
        user = SC_User.query.filter_by(id=user_id).first()
        kpi_train_operate = SC_Kpi_Train_Operate.query.filter_by(index=index,user_id=user_id).first()
        return render_template("Performance/ygpgkh/sjczpg.html",user=user,index=index,kpi_train_operate=kpi_train_operate)
    else:
        try:
            kpi_train_operate = SC_Kpi_Train_Operate.query.filter_by(index=index,user_id=user_id).first()
            if kpi_train_operate:
                kpi_train_operate.job_tendency = request.form['job_tendency']
                kpi_train_operate.index = index
                kpi_train_operate.assess_date = request.form['assess_date']
                kpi_train_operate.marketing_plain = request.form['marketing_plain']
                kpi_train_operate.marketing_complete = request.form['marketing_complete']
                kpi_train_operate.marketing_score = request.form['marketing_score']
                kpi_train_operate.sign_plain = request.form['sign_plain']
                kpi_train_operate.sign_complete = request.form['sign_complete']
                kpi_train_operate.sign_score = request.form['sign_score']
                kpi_train_operate.loan_balance_plain = request.form['loan_balance_plain']
                kpi_train_operate.loan_balance_complete = request.form['loan_balance_complete']
                kpi_train_operate.loan_balance_score = request.form['loan_balance_score']
                kpi_train_operate.monitor_plain = request.form['monitor_plain']
                kpi_train_operate.monitor_complete = request.form['monitor_complete']
                kpi_train_operate.monitor_score = request.form['monitor_score']
                kpi_train_operate.ywdlx = request.form['ywdlx']
                kpi_train_operate.yxnl = request.form['yxnl']
                kpi_train_operate.dqdc = request.form['dqdc']
                kpi_train_operate.sdhcs = request.form['sdhcs']
                kpi_train_operate.jszs = request.form['jszs']
                kpi_train_operate.khfw = request.form['khfw']
                kpi_train_operate.kqjl = request.form['kqjl']
                kpi_train_operate.zrx = request.form['zrx']
                kpi_train_operate.gtxt = request.form['gtxt']
                kpi_train_operate.tdxz = request.form['tdxz']
                kpi_train_operate.total = request.form['total']
                kpi_train_operate.result = request.form['result']
                kpi_train_operate.performance = request.form['performance']
                kpi_train_operate.focus_on = request.form['focus_on']
                kpi_train_operate.next_work_target = request.form['next_work_target']
                kpi_train_operate.individual_expectations = request.form['individual_expectations']
                kpi_train_operate.user_id = user_id
                kpi_train_operate.date_1 = datetime.datetime.now()
                kpi_train_operate.manager = current_user.id
                kpi_train_operate.date_2 = datetime.datetime.now()
            else:
                SC_Kpi_Train_Operate(request.form['job_tendency'],index,request.form['assess_date'],request.form['marketing_plain'],
                    request.form['marketing_complete'],request.form['marketing_score'],request.form['sign_plain'],
                    request.form['sign_complete'],request.form['sign_score'],request.form['loan_balance_plain'],
                    request.form['loan_balance_complete'],request.form['loan_balance_score'],request.form['monitor_plain'],
                    request.form['monitor_complete'],request.form['monitor_score'],request.form['ywdlx'],request.form['yxnl'],
                    request.form['dqdc'],request.form['sdhcs'],request.form['jszs'],request.form['khfw'],request.form['kqjl'],
                    request.form['zrx'],request.form['gtxt'],request.form['tdxz'],request.form['total'],request.form['result'],
                    request.form['performance'],request.form['focus_on'],request.form['next_work_target'],request.form['individual_expectations'],
                    user_id,datetime.datetime.now(),current_user.id,datetime.datetime.now()).add()

            #同时修改SC_Kpi_Train_Final表
            kpi_train_final = SC_Kpi_Train_Final.query.filter_by(user_id=user_id).first()
            if kpi_train_final:
                if index == 1:
                    kpi_train_final.score_2 = request.form['total']
                elif index == 2:
                    kpi_train_final.score_3 = request.form['total']
                elif index == 3:
                    kpi_train_final.score_4 = request.form['total']
            else:
                kpi_train_final = SC_Kpi_Train_Final(user_id)
                kpi_train_final.add()
                db.session.flush()
                if index == 1:
                    kpi_train_final.score_2 = request.form['total']
                elif index == 2:
                    kpi_train_final.score_3 = request.form['total']
                elif index == 3:
                    kpi_train_final.score_4 = request.form['total']

            # 事务提交
            db.session.commit()
            # 消息闪现
            flash('保存成功','success')
        except:
            # 回滚
            db.session.rollback()
            logger.exception('exception')
            # 消息闪现
            flash('保存失败','error')

        return redirect('Performance/ygpgkh/pxqpglist')

# 最终评估
@app.route('/Performance/ygpgkh/zzpg/<int:user_id>', methods=['GET','POST'])
def zzpg(user_id):
    if request.method == 'GET':
        user = SC_User.query.filter_by(id=user_id).first()
        kpi_train_final = SC_Kpi_Train_Final.query.filter_by(user_id=user_id).first()
        return render_template("Performance/ygpgkh/zzpg.html",user=user,kpi_train_final=kpi_train_final)
    else:
        try:
            kpi_train_final = SC_Kpi_Train_Final.query.filter_by(user_id=user_id).first()
            if kpi_train_final:
                kpi_train_final.job_tendency = request.form['job_tendency']
                kpi_train_final.training_cycle = request.form['training_cycle']
                kpi_train_final.job_final = request.form['job_final']

                kpi_train_final.total_score = request.form['total_score']
                kpi_train_final.avg_score = request.form['avg_score']

                kpi_train_final.zpj = request.form['zpj']
                kpi_train_final.is_ok = request.form['is_ok']
                kpi_train_final.jyyqw = request.form['jyyqw']

                kpi_train_final.user_id = user_id
                kpi_train_final.date_1 = datetime.datetime.now()
                kpi_train_final.manager = current_user.id
                kpi_train_final.date_2 = datetime.datetime.now()

            # 事务提交
            db.session.commit()
            # 消息闪现
            flash('保存成功','success')
        except:
            # 回滚
            db.session.rollback()
            logger.exception('exception')
            # 消息闪现
            flash('保存失败','error')

        return redirect('Performance/ygpgkh/pxqpglist')



# 在岗评估——搜索
@app.route('/Performance/ygpgkh/zgpg_search', methods=['GET'])
def zgpg_search():
    return render_template("Performance/ygpgkh/zgpg_search.html")

# 在岗评估列表
@app.route('/Performance/ygpgkh/zgpglist', methods=['GET'])
def zgpglist():
    return render_template("Performance/ygpgkh/zgpglist.html")

# 在岗评估
@app.route('/Performance/ygpgkh/zgpg', methods=['GET'])
def zgpg():
    return render_template("Performance/ygpgkh/zgpg.html")

# 新增客户经理KPI
@app.route('/Performance/ygpgkh/new_khjlKPI', methods=['GET'])
def new_khjlKPI():
    return render_template("Performance/ygpgkh/new_khjlKPI.html")

# 新增后台岗KPI
@app.route('/Performance/ygpgkh/new_htgKPI', methods=['GET'])
def new_htgKPI():
    return render_template("Performance/ygpgkh/new_htgKPI.html")
