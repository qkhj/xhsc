# coding:utf-8

import os

from flask import Module, session, request, render_template, redirect, url_for,flash,send_from_directory,send_file
from flask.ext.login import current_user
import datetime
import urllib2 

from scapp.config import LOCALDB_FOLDER_REL
from scapp.config import LOCALDB_FOLDER_ABS
from scapp.config import logger
from scapp.config import PER_PAGE

from scapp.models.data.sc_localdb import SC_LocalDB

from scapp import db
from scapp import app
import sqlite3

from scapp.models import SC_User


from scapp.models import SC_Loan_Apply
from scapp.models import SC_Apply_Info
from scapp.models import SC_Co_Borrower
from scapp.models import SC_Guaranty
from scapp.models import SC_Guarantees

from scapp.models.credit_data.sc_balance_sheet import SC_Balance_Sheet
from scapp.models.credit_data.sc_cross_examination import SC_Cross_Examination
from scapp.models.credit_data.sc_cash_flow import SC_Cash_Flow
from scapp.models.credit_data.sc_cash_flow_assist import SC_Cash_Flow_Assist
from scapp.models.credit_data.sc_cash_flow_dec import SC_Cash_Flow_Dec
from scapp.models.credit_data.sc_profit_loss import SC_Profit_Loss
from scapp.models.credit_data.sc_stock import SC_Stock
from scapp.models.credit_data.sc_profit_jcjy import SC_Profit_Jcjy
from scapp.models.credit_data.sc_dydb_dec import SC_Dydb_Dec

from scapp.models import SC_Loan_Product
from scapp.models import View_Query_Loan

from scapp.logic.total import AssetsList
from scapp.logic.total import Examine

from scapp.config import PROCESS_STATUS_DKFKJH

# 导入本地数据-贷款列表 
@app.route('/Data/drbdsj', methods=['GET'])
def drbdsj():
    try:
        localdb = SC_LocalDB.query.filter_by(user_id=current_user.id).first()
        if localdb:
            cx = sqlite3.connect(os.path.join(LOCALDB_FOLDER_ABS,'%d\\%s' % (current_user.id,localdb.attachment)))
            cu=cx.cursor()
            cu.execute("select * from sc_customer")
            customers = cu.fetchall()  
            if customers:
                flash('查询导入数据成功','success')
                return render_template("Data/drbdsj.html",customers=customers)
            else:
                flash('未查询到导入数据','error')
            return render_template("Data/drbdsj.html")
        else:
            flash('未查询到导入数据','error')
            return render_template("Data/drbdsj.html")
    except:
        logger.exception('exception')
        # 消息闪现
        flash('查询导入数据失败','error')
        
        return render_template("Data/drbdsj.html")
            
# 导入本地数据-搜索
@app.route('/Data/drbdsj_import', methods=['GET'])
def drbdsj_import():
    return render_template("Data/drbdsj_import.html")    

# 导入本地数据-搜索
@app.route('/Data/import', methods=['POST'])
def data_import():
    if request.method == 'POST':
        try:
            # 先获取上传文件
            f = request.files['attachment']
            fname = f.filename
            if not os.path.exists(os.path.join(LOCALDB_FOLDER_ABS,str(current_user.id))):
                os.mkdir(os.path.join(LOCALDB_FOLDER_ABS,str(current_user.id)))
            f.save(os.path.join(LOCALDB_FOLDER_ABS,'%d\\%s' % (current_user.id,fname)))
            
            SC_LocalDB.query.filter_by(user_id=current_user.id).delete()
            db.session.flush()
            
            SC_LocalDB(current_user.id,fname).add()
            
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
            
        return redirect("Data/drbdsj")

# 数据同步-搜索
@app.route('/Data/sjtb_search', methods=['GET'])
def sjtb_search():
    loan_product = SC_Loan_Product.query.all()
    return render_template("Data/sjtb_search.html",loan_product=loan_product)  
    
# 数据同步-列表
@app.route('/Data/sjtbList/<int:page>', methods=['GET','POST'])
def sjtbList(page):
    customer_name = request.form['customer_name']
    loan_type = request.form['loan_type']
    sql = ""
    if loan_type != '0':
        sql = "loan_type='"+loan_type+"' and "
    sql += " marketing_loan_officer="+str(current_user.id)+" and (process_status<>'"+PROCESS_STATUS_DKFKJH+"')"

    if customer_name:
        sql += " and (company_customer_name like '%"+customer_name+"%' or individual_customer_name like '%"+customer_name+"%')"

    loan_apply = View_Query_Loan.query.filter(sql).paginate(page, per_page = PER_PAGE)
    loan_product = SC_Loan_Product.query.all()
    
    customers = None
    localdb = SC_LocalDB.query.filter_by(user_id=current_user.id).first()
    if localdb:
        cx = sqlite3.connect(os.path.join(LOCALDB_FOLDER_ABS,'%d\\%s' % (current_user.id,localdb.attachment)))
        cu=cx.cursor()
        cu.execute("select * from sc_customer")
        customers = cu.fetchall()
        
    return render_template("Data/sjtbList.html",loan_apply=loan_apply,customer_name=customer_name,loan_type=loan_type,loan_product=loan_product,customers=customers)

# 数据同步
@app.route('/Data/sjtb/<int:loan_apply_id>/<int:localid>', methods=['GET'])
def sjtb(loan_apply_id,localid):
    loan_apply = SC_Loan_Apply.query.filter_by(id=loan_apply_id).first()
    loan_product = SC_Loan_Product.query.all()
    return render_template("Data/sjtb.html",loan_apply=loan_apply,loan_product=loan_product,localid=localid) 

# 数据同步-资产负债表
@app.route('/Data/data_zcfzb/<int:loan_apply_id>/<int:localid>', methods=['GET','POST'])
def data_zcfzb(loan_apply_id,localid):
    if request.method == 'GET':
        sc_balance_sheet = None
        localdb = SC_LocalDB.query.filter_by(user_id=current_user.id).first()
        if localdb:
            cx = sqlite3.connect(os.path.join(LOCALDB_FOLDER_ABS,'%d\\%s' % (current_user.id,localdb.attachment)))
            cu=cx.cursor()
            cu.execute("select * from sc_balance_sheet where customer_id="+str(localid))
            sc_balance_sheet = cu.fetchone()
        return render_template("Data/dqdcXed_zcfzb.html",loan_apply_id=loan_apply_id,localid=localid,sc_balance_sheet=sc_balance_sheet) 
    else:
        try:
            SC_Balance_Sheet.query.filter_by(loan_apply_id=loan_apply_id).delete()
            db.session.flush()

            for i in range(34):
                print '111'
                for j in range(len(request.form.getlist('type_%s' % i))):
                    SC_Balance_Sheet(loan_apply_id,i,request.form.getlist('name_%s' % i)[j],
                        j,request.form.getlist('value_%s' % i)[j]).add()
            
            
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
            
        return redirect('Data/sjtb/%d/%d' % (loan_apply_id,localid))

# 数据同步-交叉检验
@app.route('/Data/data_jcjy/<int:loan_apply_id>/<int:localid>', methods=['GET','POST'])
def data_jcjy(loan_apply_id,localid):
    if request.method == 'GET':
        sc_cross_examination = None
        localdb = SC_LocalDB.query.filter_by(user_id=current_user.id).first()
        if localdb:
            cx = sqlite3.connect(os.path.join(LOCALDB_FOLDER_ABS,'%d\\%s' % (current_user.id,localdb.attachment)))
            cu=cx.cursor()
            cu.execute("select * from sc_cross_examination where customer_id="+str(localid))
            sc_cross_examination = cu.fetchone()
        return render_template("Data/dqdcXed_jcjy.html",loan_apply_id=loan_apply_id,localid=localid,sc_cross_examination=sc_cross_examination)  
    else:
        try:
            SC_Cross_Examination.query.filter_by(loan_apply_id=loan_apply_id).delete()
            db.session.flush()

            for i in range(15):
                for j in range(len(request.form.getlist('type_%s' % i))):
                    SC_Cross_Examination(loan_apply_id,i,request.form.getlist('name_%s' % i)[j],
                        j,request.form.getlist('value_%s' % i)[j]).add()
                        
            #修改毛利润录入方式
            SC_Profit_Jcjy.query.filter_by(loan_apply_id=loan_apply_id).delete()
            db.session.flush()
            
            if request.form['record_type'] == '2':#录入详细数据
                names = request.form.getlist('name')
                types = request.form.getlist('type')
                bids = request.form.getlist('bid')
                prices = request.form.getlist('price')
                ratios = request.form.getlist('ratio')
                profits = request.form.getlist('profit')
                
                index1 = -1#递增序列
                index2 = -1#递增序列
                for i in range(len(names)):
                    if types[i] == '1':
                        index1 = index1 + 1
                        index = index1
                    if types[i] == '2':
                        index = index1
                    if types[i] == '3':
                        index2 = index2 + 1
                        index = index2
                    if types[i] == '4':
                        index = None
                    SC_Profit_Jcjy(loan_apply_id,types[i],index,names[i],bids[i],prices[i],ratios[i],profits[i]).add()
                
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

        return redirect('Data/sjtb/%d/%d' % (loan_apply_id,localid))

# 数据同步-交叉检验
@app.route('/Data/data_ysqkfx/<int:loan_apply_id>/<int:localid>', methods=['GET','POST'])
def data_ysqkfx(loan_apply_id,localid):
    if request.method == 'GET':
        sc_profit_loss = None
        localdb = SC_LocalDB.query.filter_by(user_id=current_user.id).first()
        if localdb:
            cx = sqlite3.connect(os.path.join(LOCALDB_FOLDER_ABS,'%d\\%s' % (current_user.id,localdb.attachment)))
            cu=cx.cursor()
            cu.execute("select * from sc_profit_loss where customer_id="+str(localid))
            sc_profit_loss = cu.fetchone()
        return render_template("Data/dqdcXed_ysqkfx.html",loan_apply_id=loan_apply_id,localid=localid,sc_profit_loss=sc_profit_loss)  
    else:
        try:
            SC_Profit_Loss.query.filter_by(loan_apply_id=loan_apply_id).delete()
            db.session.flush()

            for i in range(31):
                for j in range(len(request.form.getlist('items_name_%s' % i))):
                    SC_Profit_Loss(loan_apply_id,i,request.form.getlist('items_name_%s' % i)[j],
                        j,request.form.getlist('month_1_%s' % i)[j],request.form.getlist('month_2_%s' % i)[j],
                        request.form.getlist('month_3_%s' % i)[j],request.form.getlist('month_4_%s' % i)[j],
                        request.form.getlist('month_5_%s' % i)[j],request.form.getlist('month_6_%s' % i)[j],
                        request.form.getlist('month_7_%s' % i)[j],request.form.getlist('month_8_%s' % i)[j],
                        request.form.getlist('month_9_%s' % i)[j],request.form.getlist('month_10_%s' % i)[j],
                        request.form.getlist('month_11_%s' % i)[j],request.form.getlist('month_12_%s' % i)[j],
                        request.form.getlist('total_%s' % i)[j],request.form.getlist('pre_month_%s' % i)[j]).add()

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
            
        return redirect('Data/sjtb/%d/%d' % (loan_apply_id,localid))

# 数据同步-现金流分析
@app.route('/Data/data_xjlfx/<int:loan_apply_id>/<int:localid>', methods=['GET','POST'])
def data_xjlfx(loan_apply_id,localid):
    if request.method == 'GET':
        sc_cash_flow = None
        localdb = SC_LocalDB.query.filter_by(user_id=current_user.id).first()
        if localdb:
            cx = sqlite3.connect(os.path.join(LOCALDB_FOLDER_ABS,'%d\\%s' % (current_user.id,localdb.attachment)))
            cu=cx.cursor()
            cu.execute("select * from sc_cash_flow where customer_id="+str(localid))
            sc_cash_flow = cu.fetchone()
        return render_template("Data/dqdcXed_xjlfx.html",loan_apply_id=loan_apply_id,localid=localid,sc_cash_flow=sc_cash_flow)
    else:
        try:
            id=loan_apply_id
            #保存现金流
            cash_flow = SC_Cash_Flow.query.filter_by(loan_apply_id=id,type=1).order_by("id").all()
    
            early_cash_list = request.form.getlist('early_cash')
            sale_amount_list = request.form.getlist('sale_amount')
            accounts_receivable_list = request.form.getlist('accounts_receivable')
            prepaments_list = request.form.getlist('prepaments')
            total_cash_flow_list = request.form.getlist('total_cash_flow')
            cash_purchase_list = request.form.getlist('cash_purchase')
            accounts_payable_list = request.form.getlist('accounts_payable')
            advance_purchases_list = request.form.getlist('advance_purchases')
            total_cash_outflow_list = request.form.getlist('total_cash_outflow')
            wage_labor_list = request.form.getlist('wage_labor')
            tax_list = request.form.getlist('tax')
            transportation_costs_list = request.form.getlist('transportation_costs')
            rent_list = request.form.getlist('rent')
            maintenance_fees_list = request.form.getlist('maintenance_fees')
            utility_bills_list = request.form.getlist('utility_bills')
            advertising_fees_list = request.form.getlist('advertising_fees')
            social_intercourse_fees_list = request.form.getlist('social_intercourse_fees')
            fixed_costs_list = request.form.getlist('fixed_costs')
            fixed_asset_investment_list = request.form.getlist('fixed_asset_investment')
            disposal_of_fixed_assets_list = request.form.getlist('disposal_of_fixed_assets')
            investment_cash_flow_list = request.form.getlist('investment_cash_flow')
            bank_loans_list = request.form.getlist('bank_loans')
            repayments_bank_list = request.form.getlist('repayments_bank')
            financing_cash_flow_list = request.form.getlist('financing_cash_flow')
            household_expenditure_list = request.form.getlist('household_expenditure')
            private_use_list = request.form.getlist('private_use')
            private_cash_flow_list = request.form.getlist('private_cash_flow')
            ljxj_list = request.form.getlist('ljxj')
            qmxj_list = request.form.getlist('qmxj')
    
            if len(cash_flow) == 0: 
                # 循环获取表单
                for i in range(len(early_cash_list)):
                    SC_Cash_Flow(id,1,i,
                        early_cash_list[i],sale_amount_list[i],
                        accounts_receivable_list[i],prepaments_list[i],
                        total_cash_flow_list[i],cash_purchase_list[i],
                        accounts_payable_list[i],advance_purchases_list[i],
                        total_cash_outflow_list[i],wage_labor_list[i],
                        tax_list[i],transportation_costs_list[i],
                        rent_list[i],maintenance_fees_list[i],
                        utility_bills_list[i],advertising_fees_list[i],
                        social_intercourse_fees_list[i],fixed_costs_list[i],
                        fixed_asset_investment_list[i],disposal_of_fixed_assets_list[i],
                        investment_cash_flow_list[i],
                        bank_loans_list[i],repayments_bank_list[i],
                        financing_cash_flow_list[i],household_expenditure_list[i],
                        private_use_list[i],private_cash_flow_list[i],
                        ljxj_list[i],qmxj_list[i]).add()
            else:
                for i in range(0, 13):
                    SC_Cash_Flow.query.filter_by(loan_apply_id=id,type=1,month=i).update({
                        "early_cash":early_cash_list[i],"sale_amount":sale_amount_list[i],
                        "accounts_receivable":accounts_receivable_list[i],"prepaments":prepaments_list[i],
                        "total_cash_flow":total_cash_flow_list[i],"cash_purchase":cash_purchase_list[i],
                        "accounts_payable":accounts_payable_list[i],"advance_purchases":advance_purchases_list[i],
                        "total_cash_outflow":total_cash_outflow_list[i],"wage_labor":wage_labor_list[i],
                        "tax":tax_list[i],"transportation_costs":transportation_costs_list[i],
                        "rent":rent_list[i],"maintenance_fees":maintenance_fees_list[i],
                        "utility_bills":utility_bills_list[i],"advertising_fees":advertising_fees_list[i],
                        "social_intercourse_fees":social_intercourse_fees_list[i],"fixed_costs":fixed_costs_list[i],
                        "fixed_asset_investment":fixed_asset_investment_list[i],"disposal_of_fixed_assets":disposal_of_fixed_assets_list[i],
                        "investment_cash_flow":investment_cash_flow_list[i],
                        "bank_loans":bank_loans_list[i],"repayments_bank":repayments_bank_list[i],
                        "financing_cash_flow":financing_cash_flow_list[i],"household_expenditure":household_expenditure_list[i],
                        "private_use":private_use_list[i],"private_cash_flow":private_cash_flow_list[i],
                        "ljxj":ljxj_list[i],"qmxj":qmxj_list[i]})
    
                #保存现金流其他信息
                name_cash_flow_assist_0_list = request.form.getlist('name_cash_flow_assist_0')
                name_cash_flow_assist_1_list = request.form.getlist('name_cash_flow_assist_1')
                name_cash_flow_assist_2_list = request.form.getlist('name_cash_flow_assist_2')
                name_cash_flow_assist_3_list = request.form.getlist('name_cash_flow_assist_3')
                len0 = len(name_cash_flow_assist_0_list)
                len1 = len(name_cash_flow_assist_1_list)
                len2 = len(name_cash_flow_assist_2_list)
                len3 = len(name_cash_flow_assist_3_list)
        
                month_0_list = request.form.getlist('month_0')
                month_1_list = request.form.getlist('month_1')
                month_2_list = request.form.getlist('month_2')
                month_3_list = request.form.getlist('month_3')
                month_4_list = request.form.getlist('month_4')
                month_5_list = request.form.getlist('month_5')
                month_6_list = request.form.getlist('month_6')
                month_7_list = request.form.getlist('month_7')
                month_8_list = request.form.getlist('month_8')
                month_9_list = request.form.getlist('month_9')
                month_10_list = request.form.getlist('month_10')
                month_11_list = request.form.getlist('month_11')
                month_12_list = request.form.getlist('month_12')
        
                SC_Cash_Flow_Assist.query.filter_by(loan_apply_id=id,type=1,assist_type=0).delete()
                db.session.flush()
                for i in range(0,len0):
                    SC_Cash_Flow_Assist(id,1,0,name_cash_flow_assist_0_list[i],month_0_list[i],
                        month_1_list[i],month_2_list[i],month_3_list[i],month_4_list[i],month_5_list[i],
                        month_6_list[i],month_7_list[i],month_8_list[i],month_9_list[i],month_10_list[i],
                        month_11_list[i],month_12_list[i]).add()
        
                SC_Cash_Flow_Assist.query.filter_by(loan_apply_id=id,type=1,assist_type=1).delete()
                db.session.flush()
                for i in range(len0,len0+len1):
                    SC_Cash_Flow_Assist(id,1,1,name_cash_flow_assist_1_list[i-len0],month_0_list[i],
                        month_1_list[i],month_2_list[i],month_3_list[i],month_4_list[i],month_5_list[i],
                        month_6_list[i],month_7_list[i],month_8_list[i],month_9_list[i],month_10_list[i],
                        month_11_list[i],month_12_list[i]).add()
        
                SC_Cash_Flow_Assist.query.filter_by(loan_apply_id=id,type=1,assist_type=2).delete()
                db.session.flush()
                for i in range(len0+len1,len0+len1+len2):
                    SC_Cash_Flow_Assist(id,1,2,name_cash_flow_assist_2_list[i-len0-len1],month_0_list[i],
                        month_1_list[i],month_2_list[i],month_3_list[i],month_4_list[i],month_5_list[i],
                        month_6_list[i],month_7_list[i],month_8_list[i],month_9_list[i],month_10_list[i],
                        month_11_list[i],month_12_list[i]).add()
        
                SC_Cash_Flow_Assist.query.filter_by(loan_apply_id=id,type=1,assist_type=3).delete()
                db.session.flush()
                for i in range(len0+len1+len2,len0+len1+len2+len3):
                    #print i-len0-len1-len2
                    SC_Cash_Flow_Assist(id,1,3,name_cash_flow_assist_3_list[i-len0-len1-len2],month_0_list[i],
                        month_1_list[i],month_2_list[i],month_3_list[i],month_4_list[i],month_5_list[i],
                        month_6_list[i],month_7_list[i],month_8_list[i],month_9_list[i],month_10_list[i],
                        month_11_list[i],month_12_list[i]).add()
        
                cash_flow_dec = SC_Cash_Flow_Dec.query.filter_by(loan_apply_id=id).first()
                if cash_flow_dec:
                    cash_flow_dec.dec_1 = request.form['dec_1']
                    cash_flow_dec.dec_2 = request.form['dec_2']
                else:
                    SC_Cash_Flow_Dec(id,request.form['dec_1'],request.form['dec_2']).add()
        
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
    
        return redirect('Data/sjtb/%d/%d' % (loan_apply_id,localid))

# 数据同步-担保抵押调查表
@app.route('/Data/data_dbdydcb/<int:loan_apply_id>/<int:localid>', methods=['GET','POST'])
def data_dbdydcb(loan_apply_id,localid):
    if request.method == 'GET':
        sc_dbdydcb = None
        localdb = SC_LocalDB.query.filter_by(user_id=current_user.id).first()
        if localdb:
            cx = sqlite3.connect(os.path.join(LOCALDB_FOLDER_ABS,'%d\\%s' % (current_user.id,localdb.attachment)))
            cu=cx.cursor()
            cu.execute("select * from sc_dbdydcb where customer_id="+str(localid))
            sc_dbdydcb = cu.fetchone()
        return render_template("Data/dqdcXed_dbdydcb.html",loan_apply_id=loan_apply_id,localid=localid,sc_dbdydcb=sc_dbdydcb)
    else:
        try:
            id = loan_apply_id
            #保存共同借款人
            SC_Co_Borrower.query.filter_by(loan_apply_id=id).delete()
            db.session.flush()
            name_list = request.form.getlist('name')
            relationship_list = request.form.getlist('relationship')
            id_number_list = request.form.getlist('id_number')
            phone_list = request.form.getlist('phone')
            main_business_list = request.form.getlist('main_business')
            address_list = request.form.getlist('address')
            major_assets_list = request.form.getlist('major_assets')
            monthly_income_list = request.form.getlist('monthly_income')
            major_assets_list = request.form.getlist('major_assets')
            monthly_income_list = request.form.getlist('monthly_income')
            home_addr_list = request.form.getlist('home_addr')
            hj_addr_list = request.form.getlist('hj_addr')
            home_list = request.form.getlist('home')
            remark_list = request.form.getlist('remark')
            # 循环获取表单
            for i in range(len(name_list)):
                SC_Co_Borrower(id,name_list[i],relationship_list[i],
                    id_number_list[i],phone_list[i],main_business_list[i],
                    address_list[i],major_assets_list[i],monthly_income_list[i],
                    home_addr_list[i],hj_addr_list[i],home_list[i],remark_list[i]).add()
    
            #保存担保信息
            SC_Guarantees.query.filter_by(loan_apply_id=id).delete()
            db.session.flush()
            name_db_list = request.form.getlist('name_db')
            address_db_list = request.form.getlist('address_db')
            id_number_db_list = request.form.getlist('id_number_db')
            workunit_db_list = request.form.getlist('workunit_db')
            phone_db_list = request.form.getlist('phone_db')
            relationship_db_list = request.form.getlist('relationship_db')
            major_assets_db_list = request.form.getlist('major_assets_db')
            monthly_income_db_list = request.form.getlist('monthly_income_db')
            home_addr_db_list = request.form.getlist('home_addr_db')
            hj_addr_db_list = request.form.getlist('hj_addr_db')
            home_db_list = request.form.getlist('home_db')
            remark_db_list = request.form.getlist('remark_db')
            # 循环获取表单
            for i in range(len(name_db_list)):
                SC_Guarantees(id,name_db_list[i],address_db_list[i],
                    id_number_db_list[i],workunit_db_list[i],phone_db_list[i],
                    relationship_db_list[i],major_assets_db_list[i],monthly_income_db_list[i],
                    home_addr_db_list[i],hj_addr_db_list[i],home_db_list[i],remark_db_list[i]).add()
    
            #保存有无抵押物
            SC_Guaranty.query.filter_by(loan_apply_id=id).delete()
            db.session.flush()
            obj_name_list = request.form.getlist('obj_name')
            owner_address_list = request.form.getlist('owner_address')
            description_list = request.form.getlist('description')
            registration_number_list = request.form.getlist('registration_number')
            appraisal_list = request.form.getlist('appraisal')
            mortgage_list = request.form.getlist('mortgage')
            # 循环获取表单
            for i in range(len(obj_name_list)):
                SC_Guaranty(id,obj_name_list[i],owner_address_list[i],
                    description_list[i],registration_number_list[i],appraisal_list[i],
                    mortgage_list[i],0).add()
    
            dydb_dec = SC_Dydb_Dec.query.filter_by(loan_apply_id=id).first()
            if dydb_dec:
                dydb_dec.dec = request.form['dec']
            else:
                SC_Dydb_Dec(id,request.form['dec']).add()
    
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
    
        return redirect('Data/sjtb/%d/%d' % (loan_apply_id,localid))

# 数据同步-固定资产清单
@app.route('/Data/data_gdzcqd/<int:loan_apply_id>/<int:localid>', methods=['GET','POST'])
def data_gdzcqd(loan_apply_id,localid):
    if request.method == 'GET':
        sc_gdzcqd = None
        localdb = SC_LocalDB.query.filter_by(user_id=current_user.id).first()
        if localdb:
            cx = sqlite3.connect(os.path.join(LOCALDB_FOLDER_ABS,'%d\\%s' % (current_user.id,localdb.attachment)))
            cu=cx.cursor()
            cu.execute("select * from sc_gdzcqd where customer_id="+str(localid))
            sc_gdzcqd = cu.fetchone()
        return render_template("Data/dqdcXed_gdzcqd.html",loan_apply_id=loan_apply_id,localid=localid,sc_gdzcqd=sc_gdzcqd)
    else:
        assets = AssetsList()
        assets.addList(loan_apply_id,request)
        
        return redirect('Data/sjtb/%d/%d' % (loan_apply_id,localid))

# 数据同步-库存
@app.route('/Data/data_kc/<int:loan_apply_id>/<int:localid>', methods=['GET','POST'])
def data_kc(loan_apply_id,localid):
    if request.method == 'GET':
        sc_stock = None
        localdb = SC_LocalDB.query.filter_by(user_id=current_user.id).first()
        if localdb:
            cx = sqlite3.connect(os.path.join(LOCALDB_FOLDER_ABS,'%d\\%s' % (current_user.id,localdb.attachment)))
            cu=cx.cursor()
            cu.execute("select * from sc_stock where customer_id="+str(localid))
            sc_stock = cu.fetchone()
        return render_template("Data/dqdcXed_kc.html",loan_apply_id=loan_apply_id,localid=localid,sc_stock=sc_stock)
    else:
        try:
            SC_Stock.query.filter_by(loan_apply_id=loan_apply_id).delete()
            db.session.flush()
    
            name_list = request.form.getlist('name')
            amount_list = request.form.getlist('amount')
            purchase_price_list = request.form.getlist('purchase_price')
            purchase_total_price_list = request.form.getlist('purchase_total_price')
    
            # 循环获取表单
            for i in range(len(name_list)):
                SC_Stock(loan_apply_id,name_list[i],amount_list[i],
                    purchase_price_list[i],purchase_total_price_list[i],None,None,None).add()
    
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
            
        return redirect('Data/sjtb/%d/%d' % (loan_apply_id,localid))

# 数据同步-账款清单
@app.route('/Data/data_zkqd/<int:loan_apply_id>/<int:localid>', methods=['GET','POST'])
def data_zkqd(loan_apply_id,localid):
    if request.method == 'GET':
        sc_zkqd = None
        localdb = SC_LocalDB.query.filter_by(user_id=current_user.id).first()
        if localdb:
            cx = sqlite3.connect(os.path.join(LOCALDB_FOLDER_ABS,'%d\\%s' % (current_user.id,localdb.attachment)))
            cu=cx.cursor()
            cu.execute("select * from sc_zkqd where customer_id="+str(localid))
            sc_zkqd = cu.fetchone()
        return render_template("Data/dqdcXed_zkqd.html",loan_apply_id=loan_apply_id,localid=localid,sc_zkqd=sc_zkqd)
    else:
        examine = Examine()
        #先删除所有记录
        examine.deleteList(loan_apply_id)
        #新增
        examine.addList(loan_apply_id,request)
        return redirect('Data/sjtb/%d/%d' % (loan_apply_id,localid))
    