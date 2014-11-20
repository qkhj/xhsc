#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask.ext.login import current_user

import re
import xdrlib
import xlrd
import os 
 
import Queue,time  
import types
import datetime

import sql
import json
from scapp.views.data.dbHelp import DBHelp 
	
def open_excel(file= 'file.xls'):
    try:
        data = xlrd.open_workbook(file)
        return data
    except Exception,e:
        print str(e)
		
#读取文件
def read_file(file,A_loan_officer,B_loan_officer,yunying_loan_officer,examiner_1,examiner_2,approver):
	data = open_excel(file)
	dbHelp = DBHelp()
	#sheetCount = len(data.sheets())#返回共多少sheet
	for sheet in data.sheets():
		#print sheet.name #sheet名称
		if sheet.name.find("基本") != -1:
			customer_no = GenTargetCustomer(sheet,dbHelp,file)
			customer_id = GenIndividualCustomer(sheet,dbHelp,file,customer_no)
			id = GenLoanApply(sheet,dbHelp,file,customer_id,A_loan_officer,B_loan_officer,yunying_loan_officer,examiner_1,examiner_2,approver)
			GenApplyInfo(sheet,dbHelp,file,id)
			GenOthers(sheet,dbHelp,file,id)
		if sheet.name.find("资负") != -1:
			GenZCFZB(sheet,dbHelp,file,id)
		if sheet.name.find("经营") != -1:
			GenJY(sheet,dbHelp,file,id)
		if sheet.name.find("损益") != -1:
			GenSY(sheet,dbHelp,file,id)
		if sheet.name.find("交叉") != -1:
			GenJC(sheet,dbHelp,file,id)
		if sheet.name.find("点货") != -1:
			GenDH(sheet,dbHelp,file,id)
		if sheet.name.find("固资") != -1:
			GenGDZC(sheet,dbHelp,file,id)
		# if sheet.name.find("应收") != -1:
			# GenYS(sheet,self.dbHelp,file,id)
		# if sheet.name.find("应付") != -1:
			# GenYF(sheet,self.dbHelp,file,id)
	return id

#目标客户		
def GenTargetCustomer(sheet,dbHelp,file):
	#keyMap = ["3-1","5-5","4-1","5-1"]
	customer_name = sheet.row(3)[1].value
	mobile = sheet.row(5)[5].value
	sex = 1
	if sheet.row(4)[1].value == "男":
		sex = 1
	elif sheet.row(4)[1].value == "女":
		sex = 0
	elif int(sheet.row(4)[1].value) == 2:
		sex = 0
	address = sheet.row(5)[1].value
	genSql = sql.sqlTargetCustomer.substitute(customer_name=customer_name,mobile=mobile,sex=sex,address=address)
	#return db.session.execute(genSql)
	return dbHelp.executeSql(genSql,file)

# 个人客户表
def GenIndividualCustomer(sheet,dbHelp,file,customer_no):
	#keyMap = ["3-1","4-1","4-5","5-5","8-1","5-1","5-1"]
	customer_name = sheet.row(3)[1].value
	sex = 1
	if sheet.row(4)[1].value == "男":
		sex = 1
	elif sheet.row(4)[1].value == "女":
		sex = 0
	elif int(sheet.row(4)[1].value) == 2:
		sex = 0
	credentials_no = sheet.row(4)[5].value
	mobile = sheet.row(5)[5].value
	
	# 户籍所在地所在行不确定
	nrows = sheet.nrows #行数
	ncolnames = len(sheet.row_values(0)) #列数
	for rownum in range(0,13):
		row = sheet.row_values(rownum)
		if row:
			for i in range(ncolnames):
				if row[i] == "户籍所在地":
					residence = row[i+1]
					residence_address = row[i+1]
			
	home_address = sheet.row(9)[1].value
	genSql = sql.sqlIndividualCustomer.substitute(customer_no=customer_no,customer_name=customer_name,
		sex=sex,credentials_no=credentials_no,mobile=mobile,residence=residence,
		residence_address=residence_address,home_address=home_address)
	#return db.session.execute(genSql)
	return dbHelp.executeSql(genSql,file)
	
#贷款申请主表				
def GenLoanApply(sheet,dbHelp,file,customer_id,A_loan_officer,B_loan_officer,yunying_loan_officer,examiner_1,examiner_2,approver):
	#keyMap = ["3-1"]
	customer_name = sheet.row_values(3)[1]
	genSql = sql.sqlLoanApply.substitute(belong_customer_value=customer_id,customer_name=customer_name,
		marketing_loan_officer=current_user.id,A_loan_officer=A_loan_officer,B_loan_officer=B_loan_officer,yunying_loan_officer=yunying_loan_officer,
		examiner_1=examiner_1,examiner_2=examiner_2,approver=approver,create_user=current_user.id,modify_user=current_user.id)
	#return db.session.execute(genSql)
	return dbHelp.executeSql(genSql,file)

# 申请信息表
def GenApplyInfo(sheet,dbHelp,file,id):
	# 申请信息所在行不确定
	nrows = sheet.nrows #行数
	for rownum in range(0,nrows):
		row = sheet.row_values(rownum)
		if row[0] == "申请信息":
			loan_amount_num = sheet.row_values(rownum+1)[1]
			loan_deadline = sheet.row_values(rownum+1)[4]
			details = sheet.row_values(rownum+2)[4].replace("\\","")
			break
	genSql = sql.sqlApplyInfo.substitute(loan_apply_id=id,loan_amount_num=loan_amount_num,loan_deadline=loan_deadline,details=details)
	#return db.session.execute(genSql)
	return dbHelp.executeSql(genSql,file)
	
# 其他信息
def GenOthers(sheet,dbHelp,file,id):
	#从共同借款人开始出现不对齐的情况
	#所以用关键字"共同借款人"查找
	nrows = sheet.nrows #行数
	for rownum in range(0,nrows):
		row = sheet.row_values(rownum)
		if row[0] == "信贷历史":
			GenCreditHistory(sheet,dbHelp,file,id,rownum)
		if row[0] == "共同借款人":
			GenCoBrorrower(sheet,dbHelp,file,id,rownum)
		if row[0] == "担保人":
			GenGuarantees(sheet,dbHelp,file,id,rownum)
		if row[0] == "建议抵押物":
			GenGuaranty(sheet,dbHelp,file,id,rownum)
	
# 信贷历史表
def GenCreditHistory(sheet,dbHelp,file,id,rownum):
	#keyMap = ["18-0","18-1","18-2","18-3","18-4","18-5","18-6","18-7"]
	financing_sources = sheet.row_values(rownum+3)[0]
	loan_amount = sheet.row_values(rownum+3)[1]
	deadline = sheet.row_values(rownum+3)[2]
	use = sheet.row_values(rownum+3)[3]
	temp = sheet.row(rownum+3)[4].value
	if re.match(sql.datePattern, str(temp)) is None:
		release_date = '2013-01-01'
	else:
		release_date = sheet.row(rownum+3)[4].value
	overage = sheet.row_values(rownum+3)[5]
	guarantee = sheet.row_values(rownum+3)[6]
	late_information = sheet.row_values(rownum+3)[7]
		
	genSql = sql.sqlCreditHistory.substitute(loan_apply_id=id,financing_sources=financing_sources,loan_amount=loan_amount,
				deadline=deadline,use=use,release_date=release_date,overage=overage,guarantee=guarantee,late_information=late_information)
	#db.session.execute(genSql)
	dbHelp.executeSql(genSql,file)
	
# 共同借款人
def GenCoBrorrower(sheet,dbHelp,file,id,rownum):
	#keyMap = ["?-0","?-1","?-2","?-3","?-4","?-5","?-6","?-7"]
	name = sheet.row_values(rownum+2)[0]
	relationship = sheet.row_values(rownum+2)[1]
	id_number = sheet.row_values(rownum+2)[2]
	phone = sheet.row_values(rownum+2)[3]
	main_business = sheet.row_values(rownum+2)[6]
	address = sheet.row_values(rownum+2)[5]
	monthly_income = sheet.row_values(rownum+2)[7]
	home_addr = sheet.row_values(rownum+3)[1]
	
	genSql = sql.sqlCoBrorrower.substitute(loan_apply_id=id,name=name,relationship=relationship,id_number=id_number,
				phone=phone,main_business=main_business,address=address,monthly_income=monthly_income,home_addr=home_addr)
	#db.session.execute(genSql)
	dbHelp.executeSql(genSql,file)

# 担保人
def GenGuarantees(sheet,dbHelp,file,id,rownum):
	#keyMap = ["?-0","?-1","?-2","?-3","?-4","?-5","?-6","?-7"]
	name = sheet.row_values(rownum+2)[0]
	address = sheet.row_values(rownum+3)[1]
	id_number = sheet.row_values(rownum+2)[2]
	workunit = sheet.row_values(rownum+2)[5]
	phone = sheet.row_values(rownum+2)[4]
	relationship = sheet.row_values(rownum+2)[1]
	major_assets = sheet.row_values(rownum+2)[6]
	monthly_income = sheet.row_values(rownum+2)[7]
	home_addr = sheet.row_values(rownum+3)[1]
	hj_addr = sheet.row_values(rownum+3)[6]
	genSql = sql.sqlGuarantees.substitute(loan_apply_id=id,name=name,address=address,id_number=id_number,workunit=workunit,phone=phone,
				relationship=relationship,major_assets=major_assets,monthly_income=monthly_income,home_addr=home_addr,hj_addr=hj_addr)
	#db.session.execute(genSql)
	dbHelp.executeSql(genSql,file)
	
# 抵押物
def GenGuaranty(sheet,dbHelp,file,id,rownum):
	#keyMap = ["?-0","?-1","?-2","?-3","?-4","?-5"]
	obj_name = sheet.row_values(rownum+2)[0]
	owner_address = sheet.row_values(rownum+2)[1]
	description = sheet.row_values(rownum+2)[2]
	registration_number = sheet.row_values(rownum+2)[3]
	appraisal = sheet.row_values(rownum+2)[4]
	mortgage = sheet.row_values(rownum+2)[5]
	genSql = sql.sqlGuaranty.substitute(loan_apply_id=id,obj_name=obj_name,owner_address=owner_address,description=description,
				registration_number=registration_number,appraisal=appraisal,mortgage=mortgage)
	#db.session.execute(genSql)
	dbHelp.executeSql(genSql,file)

# 资产负债表
def GenZCFZB(sheet,dbHelp,file,id):
	keyMapZCFZB_col_0 = '{"流动资产":8,"现金及银行存款":0,"应收账款":2,"预付账款":4,"存货和原材料":6,"固定资产":10,"其他资产":12,"资产总计":17,"流动比率":19}'
	keyMapZCFZB_col_2 = '{"短期负债":9,"应付账款":1,"预收账款":3,"短期贷款":5,"社会集资":7,"长期负债":11,"其他负债":13,"负债总计":15,"所有者权益":16,"负债和所有者权益总计":18,"负债率%":20,"速动比率":14}'
	#keyMapZCFZB_col_3 = ["表外资产负债情况及评价"]
	json_col_0 = json.loads(keyMapZCFZB_col_0)
	json_col_2 = json.loads(keyMapZCFZB_col_2)
	nrows = sheet.nrows #行数
	# 循环keyMapZCFZB_col_0
	index = 0
	loan_type = 0
	for rownum in range(0,nrows):
		row = sheet.row_values(rownum)
		if json_col_0.has_key(row[0]):
			index = 0
			loan_type = json_col_0.get(row[0])
		else:
			index = index + 1
		genSql = sql.sqlZCFZB.substitute(loan_apply_id=id,loan_type=loan_type,items_name=row[0],index=index,content=row[1])
		#db.session.execute(genSql)
		dbHelp.executeSql(genSql,file)
	
	# 循环keyMapZCFZB_col_2
	for rownum in range(0,nrows):
		row = sheet.row_values(rownum)
		if json_col_2.has_key(row[2]):
			index = 0
			loan_type = json_col_2.get(row[2])
		else:
			index = index + 1
		genSql = sql.sqlZCFZB.substitute(loan_apply_id=id,loan_type=loan_type,items_name=row[2],index=index,content=row[3])
		#db.session.execute(genSql)
		dbHelp.executeSql(genSql,file)
	
# 资产负债表(经营部分)
def GenJY(sheet,dbHelp,file,id):
	keyMap = ["1-0-1-1-21-经营历史和资本积累","2-0-2-1-22-生意现状（组织架构和市场）","3-0-3-1-23-生意现状（财务）",
			"4-1-4-2-26-自从上次申请后经营变化（重复贷款）生意方面","4-3-4-4-27-自从上次申请后经营变化（重复贷款）个人方面",
			"5-1-5-2-28-过去12个月的投资情况生意方面","5-3-5-4-29-过去12个月的投资情况个人方面",
			"6-1-6-2-31-未来12个月的投资计划生意方面","6-3-6-4-32-未来12个月的投资计划个人方面",
			"7-0-7-1-30-贷款目的详细描述","8-0-8-1-24-客户家庭状况（如房、车）",
			"9-0-9-1-25-对客户的印象","10-0-10-1-33-其他还款来源分析"]
	for obj in keyMap:
		obj_arr = obj.split("-")
		loan_type = obj_arr[4]
		items_name = obj_arr[5]
		try:
			content=sheet.row_values(int(obj_arr[2]))[int(obj_arr[3])]
		except Exception,ex:
			content=''
		genSql = sql.sqlZCFZB.substitute(loan_apply_id=id,loan_type=loan_type,items_name=items_name,index=0,content=content)
		#db.session.execute(genSql)
		dbHelp.executeSql(genSql,file)
	
# 损益表
def GenSY(sheet,dbHelp,file,id):
	keyMap = ["收入","可变成本","营业费用"]
	endFlag = False
	
	items_type = 0
	nrows = sheet.nrows #行数
	ncolnames = len(sheet.row_values(0)) #列数
		
	for rownum in range(2,nrows):# 从第二行开始
		index = 0
		row = sheet.row_values(rownum)
		
		if endFlag:
			break;
		if row[0] == "每月可支配资金":
			endFlag = True
			
		items_name = ""
		if row[1] != "":
			index = 0
			items_name = row[1]
		else:
			if row[0] in keyMap:
				items_type = items_type + 1
				continue
			else:
				index = index + 1
				items_name = row[0]
				
		if ncolnames < 16:#不满16列时
			nmonths = ncolnames - 4#减掉前后固定的4列
			for i in range(1,nmonths+1):
				exec("month_%d = row[%d]" % (i,i+1))
			for i in range(nmonths+1,13):
				exec("month_%d = None" % (i))
		else:
			for i in range(1,13):
				exec("month_%d = row[%d]" % (i,i+1))
		
		#for i in range(1,13):
		#	print eval("month_%d" % i)
		
		genSql = sql.sqlSY.substitute(loan_apply_id=id,items_type=items_type,items_name=items_name,index=index,
			month_1=month_1,month_2=month_2,month_3=month_3,month_4=month_4,month_5=month_5,month_6=month_6,
			month_7=month_7,month_8=month_8,month_9=month_9,month_10=month_10,month_11=month_11,month_12=month_12)	
		#db.session.execute(genSql)
		dbHelp.executeSql(genSql,file)
		
		items_type = items_type + 1
	
# 交叉检验
def GenJC(sheet,dbHelp,file,id):
	keyMap_1 = '{"销售额交叉检验":0,"毛利润/成本交叉检验":1,"其他交叉检验":2}'
	row_2 = 0#第二个map的开始行
	keyMap_2 = '{"期初权益合计":3,"分析期间收入合计":4,"大项支出合计":5,"其他收入":6,"升值":7,\
				"折旧":8,"表外资产":9,"应有权益":10,"实际权益（资产负债表所有者权益）":11,\
				"权益差额（应有权益-实际权益）":12,"分析期间累计收入":13,"权益交叉检验比率":14}'
	
	loan_type = 0
	nrows = sheet.nrows #行数
	# 循环kepMap_1
	json_keyMap_1 = json.loads(keyMap_1)
	for rownum in range(2,nrows):
		row = sheet.row_values(rownum)
		if row[0] in json_keyMap_1.keys():
			loan_type = json_keyMap_1.get(row[0])
			genSql = sql.sqlJC.substitute(loan_apply_id=id,loan_type=loan_type,items_name=row[0],index=0,content=sheet.row_values(rownum+1)[0])
			#db.session.execute(genSql)
			dbHelp.executeSql(genSql,file)
		if row[0].find("权益交叉检验") != -1:
			row_2 = rownum
			break
		
	loan_type = 0
	index = 0
	# 循环keyMap_2
	json_keyMap_2 = json.loads(keyMap_2)
	for rownum in range(row_2,nrows):
		row = sheet.row_values(rownum)
		if row[0] in json_keyMap_2.keys():
			index = 0
			loan_type = json_keyMap_2.get(row[0])
		else:
			index = index + 1
		genSql = sql.sqlJC.substitute(loan_apply_id=id,loan_type=loan_type,items_name=row[0],index=index,content=sheet.row_values(rownum)[0])
		#db.session.execute(genSql)
		dbHelp.executeSql(genSql,file)
			
# 点货
def GenDH(sheet,dbHelp,file,id):
	nrows = sheet.nrows #行数
	for rownum in range(3,nrows):
		row = sheet.row_values(rownum)
		genSql = sql.sqlDH.substitute(loan_apply_id=id,name=row[0],amount=row[1],purchase_price=row[2],purchase_total_price=row[3])
		#db.session.execute(genSql)
		dbHelp.executeSql(genSql,file)

# 固定资产
def GenGDZC(sheet,dbHelp,file,id):	
	nrows = sheet.nrows #行数
	for rownum in range(3,nrows):
		row = sheet.row_values(rownum)
		temp = row[2]
		if re.match(sql.datePattern, str(temp)) is None:
			purchase_date = '2013-01-01'
		else:
			purchase_date = row[2]
		genSql = sql.sqlGDZC.substitute(loan_apply_id=id,name=row[1],purchase_date=purchase_date,total_price=row[6],rate=row[4],total=row[5],rate_price=row[7],purchase_price=row[3])
		#db.session.execute(genSql)
		dbHelp.executeSql(genSql,file)
	
# 应收账款
def GenYS(sheet,dbHelp,file,id):
	nrows = sheet.nrows #行数
	for rownum in range(3,nrows):
		row = sheet.row_values(rownum)
		genSql = sql.sqlYSYF.substitute(loan_apply_id=id,name=row[1],original_price=row[4],occur_date=row[2],deadline=row[3],mode_type=2)
		#db.session.execute(genSql)
		dbHelp.executeSql(genSql,file)
		
# 应付账款	
def GenYF(sheet,dbHelp,file,id):
	nrows = sheet.nrows #行数
	for rownum in range(3,nrows):
		row = sheet.row_values(rownum)
		genSql = sql.sqlYSYF.substitute(loan_apply_id=id,name=row[1],original_price=row[4],occur_date=row[2],deadline=row[3],mode_type=1)
		#db.session.execute(genSql)
		dbHelp.executeSql(genSql,file)