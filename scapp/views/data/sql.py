#!/usr/bin/env python
# -*- coding: utf-8 -*- 

# 日期正则表达式
datePattern = '((^((1[8-9]\d{2})|([2-9]\d{3}))([-\/\._])(10|12|0?[13578])([-\/\._])(3[01]|[12][0-9]|0?[1-9])$)|(^((1[8-9]\d{2})|([2-9]\d{3}))([-\/\._])(11|0?[469])([-\/\._])(30|[12][0-9]|0?[1-9])$)|(^((1[8-9]\d{2})|([2-9]\d{3}))([-\/\._])(0?2)([-\/\._])(2[0-8]|1[0-9]|0?[1-9])$)|(^([2468][048]00)([-\/\._])(0?2)([-\/\._])(29)$)|(^([3579][26]00)([-\/\._])(0?2)([-\/\._])(29)$)|(^([1][89][0][48])([-\/\._])(0?2)([-\/\._])(29)$)|(^([2-9][0-9][0][48])([-\/\._])(0?2)([-\/\._])(29)$)|(^([1][89][2468][048])([-\/\._])(0?2)([-\/\._])(29)$)|(^([2-9][0-9][2468][048])([-\/\._])(0?2)([-\/\._])(29)$)|(^([1][89][13579][26])([-\/\._])(0?2)([-\/\._])(29)$)|(^([2-9][0-9][13579][26])([-\/\._])(0?2)([-\/\._])(29)$))'

from string import Template
# sc_target_customer
sqlTargetCustomer = Template("INSERT INTO `sc_target_customer` \
					(`receiver`, `reception_type`, `yingxiao_status`, `client_status`, \
					`is_apply_form`, `customer_name`, `mobile`, `sex`, `age`, \
					`address`, `industry`, `business_content`, `shop_name`, `period`, \
					`property_scope`, `monthly_sales`, `employees`, `business_type`, `is_need_loan`, \
					`loan_purpose`, `loan_amount`, `repayment_type`,`guarantee_type`, `house_property`, \
					`loan_attention`, `is_have_loan`, `is_known_xhnsh`, `business_with_xhnsh`, `is_need_service`, \
					`status`, `manager`, `loan_officer`, `bool_regisiter`, `loan_officer_date`, \
					`create_user`, `create_date`, `modify_user`, `modify_date`,`remark`) \
					VALUES \
					('1', '2', '1', '4',\
					'0', '$customer_name', '$mobile', '$sex', '', \
					'$address', NULL, '', '', '',\
					'', '', '', '3', '1',\
					'1', '', '', '', '',\
					'', '', '1', '', '',\
					NULL, '1', '1', NULL, now(),\
					NULL, now(), NULL, NULL, NULL)")
					
# sc_Individual_Customer
sqlIndividualCustomer = Template("INSERT INTO `sc_individual_customer` (\
						`manager`, `customer_no`, `customer_name`, `customer_type`,\
						`credentials_type`, `birthday`, `sex`, `credentials_no`, `credentials_org`,\
						`degree`, `education`, `marriage`, `telephone`, `mobile`,\
						`residence`, `residence_address`, `home_address`, `zip_code`, `families`,\
						`living_conditions`, `is_otherjob`, `profession`, `duty`, `title`,\
						`name_1`, `relationship_1`, `phone_1`, `name_2`, `relationship_2`,\
						`phone_2`, `name_3`, `relationship_3`, `phone_3`, `name_4`,\
						`relationship_4`, `phone_4`, `spouse_name`, `spouse_company`, `spouse_credentials_type`,\
						`spouse_credentials_no`, `spouse_phone`, `spouse_mobile`, `is_active`, `is_have_export`,\
						`create_user`, `create_date`, `modify_user`, `modify_date`) \
						VALUES \
						('1', '$customer_no', '$customer_name', 'Individual', \
						'1', NULL, '$sex', '$credentials_no', NULL,\
						'其他', '其他', '', '', '$mobile', \
						'$residence', '$residence_address', '$home_address', '225700', '', \
						'自置', '0', NULL, NULL, NULL, \
						'', '', '', '', '',\
						'', '', '', '', '', \
						'', '', '', '', '1', \
						'', '', '', '1', '0',\
						'1', now(), '1', now())")
					
# sc_loan_apply
sqlLoanApply = Template("INSERT INTO `sc_loan_apply` \
				(`loan_type`, `belong_customer_type`, `belong_customer_value`, `customer_name`,\
				`evaluation`, `marketing_loan_officer`, `A_loan_officer`, `B_loan_officer`, `yunying_loan_officer`,\
				`examiner_1`, `examiner_2`, `approver`, `process_status`, `classify`,\
				`classify_dec`, `risk_level`, `create_user`, `create_date`, `modify_user`, `modify_date`)\
				VALUES \
				('2', 'Individual', '$belong_customer_value', '$customer_name', \
				'忠厚、诚实', '$marketing_loan_officer', '$A_loan_officer', '$B_loan_officer', '$yunying_loan_officer',\
				'$examiner_1', '$examiner_2', '$approver', '601', NULL,\
				NULL, '1', '$create_user', now(), '$modify_user', now())")

# sc_apply_info
sqlApplyInfo = Template("INSERT INTO `sc_apply_info` \
				(`loan_apply_id`, `loan_amount_num`, `loan_deadline`, `month_repayment`,\
				`loan_purpose`, `details`, `repayment_source`, `repayment_type`, `annual_interest_rate`)\
				VALUES \
				('$loan_apply_id', '$loan_amount_num', '$loan_deadline', '5000', \
				'1', '$details', '', NULL, NULL)")
				
# sc_credit_history
sqlCreditHistory = Template("INSERT INTO `sc_credit_history` \
					(`loan_apply_id`, `financing_sources`, `loan_amount`, `deadline`, \
					`use`, `release_date`, `overage`, `guarantee`, `late_information`) \
					VALUES \
					('$loan_apply_id', '$financing_sources', '$loan_amount', '$deadline', \
					'$use', '$release_date', '$overage', '$guarantee', '$late_information')")
				
# sc_co_borrower
sqlCoBrorrower = Template("INSERT INTO `sc_co_borrower` \
				(`loan_apply_id`, `name`, `relationship`, `id_number`,\
				`phone`, `main_business`, `address`, `major_assets`, `monthly_income`,\
				`home_addr`, `hj_addr`, `home`, `remark`) \
				VALUES \
				('$loan_apply_id', '$name', '$relationship', '$id_number',\
				'$phone', '$main_business', '$address', '', '$monthly_income',\
				'$home_addr', NULL, NULL, NULL)")

# sc_guarantees担保人
sqlGuarantees = Template("INSERT INTO `sc_guarantees` \
				(`loan_apply_id`, `name`, `address`, `id_number`,\
				`workunit`, `phone`, `relationship`, `major_assets`, `monthly_income`,\
				`home_addr`, `hj_addr`, `home`, `remark`)\
				VALUES \
				('$loan_apply_id', '$name', '$address', '$id_number',\
				'$workunit', '$phone', '$relationship', '$major_assets', '$monthly_income',\
				'$home_addr', '$hj_addr', NULL, NULL)")

# sc_guaranty抵押物
sqlGuaranty = Template("INSERT INTO `sc_guaranty` \
			(`loan_apply_id`, `obj_name`, `owner_address`, `description`, \
			`registration_number`, `appraisal`, `mortgage`, `bool_mortgage`) \
			VALUES \
			('$loan_apply_id', '$obj_name', '$owner_address', '$description',\
			'$registration_number', '$appraisal', '$mortgage', '0')")
			
# 资产负债表
sqlZCFZB = Template("INSERT INTO `sc_balance_sheet` \
			(`loan_apply_id`, `loan_type`, `items_name`, `index`,\
			`content`, `create_user`, `create_date`, `modify_user`, `modify_date`) \
			VALUES \
			('$loan_apply_id', '$loan_type', '$items_name', '$index',\
			'$content', '1', now(), NULL, NULL)")

# 损益表
sqlSY = Template("INSERT INTO `sc_profit_loss` \
			(`loan_apply_id`, `items_type`, `items_name`, `index`,\
			`month_1`, `month_2`, `month_3`, `month_4`, `month_5`, \
			`month_6`, `month_7`, `month_8`, `month_9`, `month_10`,\
			`month_11`, `month_12`, `total`, `pre_month`, `create_user`,\
			`create_date`, `modify_user`, `modify_date`) \
			VALUES \
			('$loan_apply_id', '$items_type', '$items_name', '$index',\
			'$month_1', '$month_2', '$month_3', '$month_4', '$month_5', \
			'$month_6', '$month_7', '$month_8', '$month_9', '$month_10', \
			'$month_11', '$month_12', '0', '0', '1', \
			now(), NULL, NULL)")
			
# 交叉检验
sqlJC = Template("INSERT INTO `sc_cross_examination` \
		(`loan_apply_id`, `loan_type`, `items_name`, `index`,\
		`content`, `create_user`, `create_date`, `modify_user`, `modify_date`) \
		VALUES \
		('$loan_apply_id', '$loan_type', '$items_name', '$index',\
		'$content', '1', now(), NULL, NULL)")
	
# 点货单	
sqlDH = Template("INSERT INTO `sc_stock` \
			(`loan_apply_id`, `name`, `amount`, `purchase_price`, \
			`purchase_total_price`, `sell_price`, `sell_total_price`, `pre_rate`) \
			VALUES \
			('$loan_apply_id', '$name', '$amount', '$purchase_price',\
			'$purchase_total_price', '', '0', '0')")

# 固定资产
sqlGDZC = Template("INSERT INTO `sc_fixed_assets_equipment` \
			(`loan_apply_id`, `name`, `amount`, `type_brand`, \
			`purchase_date`, `production_date`, `total_price`, `price`, `outward`, \
			`remark`, `rate`, `total`, `rate_price`, `purchase_price`) \
			VALUES \
			('$loan_apply_id', '$name', NULL, NULL, \
			'$purchase_date', NULL, '$total_price', NULL, NULL,\
			NULL, '$rate', '$total', '$rate_price', '$purchase_price')")
			
# 应收 2/应付 1
sqlYSYF = Template("INSERT INTO `sc_accounts_list` \
			(`loan_apply_id`, `name`, `original_price`, `occur_date`, \
			`deadline`, `present_price`, `cooperation_history`, `average_period`, `trading_frequency`,\
			`turnover`, `pay_type`, `source`, `other_info`, `mode_type`) \
			VALUES \
			('$loan_apply_id', '$name', '$original_price', '$occur_date',\
			'$deadline', '00000000000', '无', '', '周',\
			'', '现金', '报刊', '', $mode_type)")		
