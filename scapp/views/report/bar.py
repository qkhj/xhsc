# coding:utf-8
from flask import Module, session, request, render_template, redirect, url_for,make_response
from scapp import app
from scapp import db
from scapp.tools.flash_pic import flash_pic

# 柱状图
@app.route('/Report/bar', methods=['GET'])
def Report_bar():
    return render_template("Report/bar.html")

@app.route('/Report/flash/export_pic',methods=['GET','POST'])
def Export_pic():
	imageData = request.form['imageData']
	exp = flash_pic()
	return exp.export(imageData,'myimg')

# 柱状图
@app.route('/Report/create/bar_3d', methods=['GET'])
def Report_create_bar_3d():
	exp = flash_pic()
	#测试sql
	data=db.session.execute("select sc_user.real_name,sum(IF (process_status = '101', 1, 0)) AS s_1, "
							"sum(IF (process_status = '201', 1, 0)) AS s_2, "
							"sum(IF (process_status = '301', 1, 0)) AS s_3, "
							"sum(IF (process_status = '401', 1, 0)) AS s_4, "
							"sum(IF (process_status = '501', 1, 0)) AS s_5, "
							"sum(IF (process_status = '601', 1, 0)) AS s_6 "
							"FROM"
							"(SELECT sc_user.id AS id,sc_role.role_level AS role_level,sc_user.real_name AS real_name "
								"FROM sc_userrole "
								"INNER JOIN sc_role ON sc_userrole.role_id = sc_role.id "
								"INNER JOIN sc_user ON sc_user.id = sc_userrole.user_id "
								"where sc_role.role_level > 1)sc_user "
							"LEFT JOIN "
							"(SELECT * FROM sc_loan_apply WHERE sc_loan_apply.create_date BETWEEN '2014-01-01' AND '2014-03-11') "
							"temp ON sc_user.id = temp.marketing_loan_officer "
							"GROUP BY sc_user.id").fetchall()
	column_text=[u'新申请',u'申请通过',u'已调查',u'调查通过',u'已上会',u'已通过']
	return exp.bar_3d(data,u"笔",column_text)

	

