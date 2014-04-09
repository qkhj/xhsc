#coding:utf-8
from flask.ext.login import login_user, logout_user, current_user, login_required, flash
from scapp.models import SC_UserRole
from scapp.models import SC_User
from scapp.models import SC_Loan_Apply
from scapp.models import SC_Approval_Decision
from scapp.pojo.waiting_work import Waiting
from scapp.config import PROCESS_STATUS_DKSQ
from scapp.config import PROCESS_STATUS_DKSQSH
from scapp.models import SC_Monitor
from scapp import db
from scapp.config import logger
from scapp.models import SC_Classify
from scapp.models import View_Query_Loan
from scapp.config import PER_PAGE
from scapp.models.credit_data.sc_accounts_list import SC_Accounts_List
from scapp.models.credit_data.sc_fixed_assets_car import SC_Fixed_Assets_Car
from scapp.models.credit_data.sc_fixed_assets_estate import SC_Fixed_Assets_Estate
from scapp.models.credit_data.sc_fixed_assets_equipment import SC_Fixed_Assets_Equipment


class Total():
#待办事项统计
    def getListSum(self, role):
        role_level = role.role_level
        waiting = Waiting()
        if role_level == 1:
            counts = SC_Loan_Apply.query.filter("process_status='" + PROCESS_STATUS_DKSQ+"'").count()
            waiting.dksqsh = counts
        if role_level == 2:
            sql = "process_status = " + PROCESS_STATUS_DKSQSH
            sql += " A_loan_officer = " + str(current_user.id) + " or "
            sql += " B_loan_officer = " + str(current_user.id) + " or "
            sql += " yunying_loan_officer = " + str(current_user.id) + ""
            counts1 = SC_Loan_Apply.query.filter(sql).count()
            waiting.dqdc = counts1
        return waiting

    #新增标准
    def addNewBZ(self, loan_apply_id, request):
        try:
            monitor_date_list = request.form.getlist('monitor_date')
            monitor_type_list = request.form.getlist('monitor_type')
            monitor_content_list = request.form.getlist('monitor_content')
            monitor_remark_list = request.form.getlist('monitor_remark')
            for i in range(len(monitor_date_list)):
                SC_Monitor(loan_apply_id, monitor_date_list[i], monitor_type_list[i], monitor_content_list[i],
                           monitor_remark_list[i]).add()
            db.session.commit()
            # 消息闪现
            flash('保存成功', 'success')
        except:
            # 回滚
            db.session.rollback()
            logger.exception('exception')
            # 消息闪现
            flash('保存失败', 'error')
        #删除所有标准

    def deleteBZ(self, loan_apply_id):
        SC_Monitor.query.filter_by(loan_apply_id=loan_apply_id).delete()
        db.session.flush()

    #通过贷款单获取合同信息
    def getInformByloadId(self, loan_apply_id):
        pactInform = SC_Approval_Decision.query.filter_by(loan_apply_id=loan_apply_id).first()
        return pactInform


class User():
#获取用户名
    def getUserName(self, id):
        user = SC_User.query.filter_by(id=id).first()
        return user.login_name


class Property():
#保存资产质量分类
    def addProperty(self, loan_apply_id, index_add, classify):
        SC_Classify(loan_apply_id, index_add, classify, '', 0).add()
        db.session.commit()

    #查询最新质量分类
    def queryLastProperty(self, loan_apply_id):
        LastProperty = SC_Classify.query.filter_by(loan_apply_id=loan_apply_id).order_by("index_add desc").first()
        return LastProperty

    #更新最新质量分类
    def updateLastProperty(self, loan_apply_id, index_add, classify):
        SC_Classify.query.filter_by(loan_apply_id=loan_apply_id, index_add=index_add).update({"classify": classify})
        db.session.commit()

    #更新最新质量分类审核
    def updateLastPropertyBysh(self, loan_apply_id, index_add, is_pass):
        SC_Classify.query.filter_by(loan_apply_id=loan_apply_id, index_add=index_add).update({"is_pass": is_pass})
        db.session.commit()

    #查询质量分类列表
    def queryList(self, customer_name, loan_type, classify, page):
        sql = " 1=1 "
        if loan_type != '0':
            sql += " and loan_type='" + loan_type + "'"
        if classify != '0':
            sql += " and classify='" + classify + "'"
        if customer_name:
            sql += " and (company_customer_name like '%" + customer_name + "%' or individual_customer_name like '%" + customer_name + "%')"
        loan_apply = View_Query_Loan.query.filter(sql).paginate(page, per_page=PER_PAGE)
        return loan_apply

#贷前调查
class Examine():
#先删除调查记录
    def deleteList(self, loan_apply_id):
        SC_Accounts_List.query.filter_by(loan_apply_id=loan_apply_id).delete()
        db.session.flush()

    #新增页面所有调查记录
    def addList(self, loan_apply_id, request):
        try:
            name_list = request.form.getlist('name')
            original_price_list = request.form.getlist('original_price')
            occur_date_list = request.form.getlist('occur_date')
            deadline_list = request.form.getlist('deadline')
            present_price_list = request.form.getlist('present_price')
            cooperation_history_list = request.form.getlist('cooperation_history')
            pay_type_list = request.form.getlist('pay_type')
            mode_type_list = request.form.getlist('mode_type')
            for i in range(len(name_list)):
                SC_Accounts_List(loan_apply_id, name_list[i], original_price_list[i], occur_date_list[i],
                                 deadline_list[i], present_price_list[i], cooperation_history_list[i], pay_type_list[i],
                                 int(mode_type_list[i])).add()
            # 事务提交
            db.session.commit()
            # 消息闪现
            flash('保存成功', 'success')
        except:
            # 回滚
            db.session.rollback()
            logger.exception('exception')
            # 消息闪现
            flash('保存失败', 'error')

#固定资产清单
class AssetsList():
    def addList(self, loan_apply_id, request):
        try:
            SC_Fixed_Assets_Car.query.filter_by(loan_apply_id=loan_apply_id).delete()
            SC_Fixed_Assets_Equipment.query.filter_by(loan_apply_id=loan_apply_id).delete()
            SC_Fixed_Assets_Estate.query.filter_by(loan_apply_id=loan_apply_id).delete()
            db.session.flush()
            name_list = request.form.getlist('name')
            purchase_date_list = request.form.getlist('purchase_date')
            purchase_price_list = request.form.getlist('purchase_price')
            rate_list = request.form.getlist('rate')
            total_list = request.form.getlist('total')
            total_price_list = request.form.getlist('total_price')
            rate_price_list = request.form.getlist('rate_price')
            mode_list = request.form.getlist('mode')
            for i in range(len(name_list)):
                #新增车辆
                if mode_list[i] == "3":
                    SC_Fixed_Assets_Car(loan_apply_id, name_list[i], purchase_date_list[i], purchase_price_list[i],
                                        rate_list[i], total_list[i], total_price_list[i], rate_price_list[i]).add()
                #新增设备
                if mode_list[i] == "2":
                    SC_Fixed_Assets_Equipment(loan_apply_id, name_list[i], purchase_date_list[i],
                                              purchase_price_list[i],
                                              rate_list[i], total_list[i], total_price_list[i],
                                              rate_price_list[i]).add()
                if mode_list[i] == "1":
                    SC_Fixed_Assets_Estate(loan_apply_id, name_list[i], purchase_date_list[i], purchase_price_list[i],
                                           rate_list[i], total_list[i], total_price_list[i], rate_price_list[i]).add()
            # 事务提交
            db.session.commit()
            # 消息闪现
            flash('保存成功', 'success')
        except:
            # 回滚
            db.session.rollback()
            logger.exception('exception')
            # 消息闪现
            flash('保存失败', 'error')