# coding:utf-8
from scapp import db
from flask.ext.login import current_user
from scapp.models import SC_UserRole

#获取客户经理及后台岗的培训期最终考核
def get_user_kpi_train_final():
	userrole=SC_UserRole.query.filter_by(user_id=current_user.id).first()
	level=userrole.role.role_level

	#主管以上看到所有人的
	if level < 2:
		sql = "select sc_user.user_id,real_name,score_1,score_2,score_3,score_4,avg_score from "
		sql += "(SELECT sc_user.id AS user_id,sc_role.role_level,sc_user.real_name FROM sc_userrole "
		sql += "INNER JOIN sc_role ON sc_userrole.role_id = sc_role.id INNER JOIN sc_user ON sc_user.id = sc_userrole.user_id "
		sql += "where sc_role.role_level >= 2)sc_user "
		sql += "left join sc_kpi_train_final on sc_user.user_id = sc_kpi_train_final.user_id"
	#客户经理和后台岗只能看到自己的
	else:
		sql = "select sc_user.user_id,real_name,score_1,score_2,score_3,score_4,avg_score from "
		sql += "(SELECT sc_user.id AS user_id,sc_role.role_level,sc_user.real_name FROM sc_userrole "
		sql += "INNER JOIN sc_role ON sc_userrole.role_id = sc_role.id INNER JOIN sc_user ON sc_user.id = sc_userrole.user_id "
		sql += "where sc_user = "+current_user.id+")sc_user "
		sql += "left join sc_kpi_train_final on sc_user.user_id = sc_kpi_train_final.user_id"

	return db.engine.execute(sql).fetchall()