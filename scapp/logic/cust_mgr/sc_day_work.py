# coding:utf-8
__author__ = 'johhny'
from scapp import db
from sqlalchemy import and_
from scapp.config import PER_PAGE
from scapp.models.cust_mgr.sc_day_work import SC_Day_Work
from scapp.models import SC_UserRole

def get_data_by_conditions(page,beg_date,end_date,user_id,current_user_id,type='NOPAGE'):
    userrole=SC_UserRole.query.filter_by(user_id=current_user_id).first()
    level=userrole.role.role_level

    if not user_id:
        if level<2:
            if type=='PAGE':
                data=SC_Day_Work.query.filter(SC_Day_Work.create_date.between(beg_date,end_date)).paginate(page, per_page = PER_PAGE)
            else:
                data=db.engine.execute("select sc_day_work.create_date,sc_user.real_name as create_user,sc_day_work.work_type,"
                                   "sc_day_work.work_type_detail,sc_day_work.beg_date,sc_day_work.end_date,"
                                   "sc_day_work.time_consume,sc_day_work.remark "
                                   "from sc_day_work "
                                   "inner join sc_user ON sc_day_work.create_user=sc_user.id "
                                   "where sc_day_work.create_date between '"+beg_date+"' AND '"+end_date+"' ")
        else:
            if type=='PAGE':
                data=SC_Day_Work.query.filter(and_(SC_Day_Work.create_date.between(beg_date,end_date),
                                                   SC_Day_Work.create_user==current_user_id)).paginate(page, per_page = PER_PAGE)
            else:
                data=db.engine.execute("select sc_day_work.create_date,sc_user.real_name as create_user,sc_day_work.work_type,"
                                   "sc_day_work.work_type_detail,sc_day_work.beg_date,sc_day_work.end_date,"
                                   "sc_day_work.time_consume,sc_day_work.remark "
                                   "from sc_day_work "
                                   "inner join sc_user ON sc_day_work.create_user=sc_user.id "
                                   "where sc_day_work.create_date between '"+beg_date+"' AND '"+end_date+"' "
                                   "AND sc_day_work.create_user='"+str(current_user_id)+"'")
    else:
        if type=='PAGE':
            data=SC_Day_Work.query.filter(and_(SC_Day_Work.create_date.between(beg_date,end_date),
                                          SC_Day_Work.create_user==user_id)).paginate(page, per_page = PER_PAGE)
        else:
            data=db.engine.execute("select sc_day_work.create_date,sc_user.real_name as create_user,sc_day_work.work_type,"
                                   "sc_day_work.work_type_detail,sc_day_work.beg_date,sc_day_work.end_date,"
                                   "sc_day_work.time_consume,sc_day_work.remark "
                                   "from sc_day_work "
                                   "inner join sc_user ON sc_day_work.create_user=sc_user.id "
                                   "where sc_day_work.create_date between '"+beg_date+"' AND '"+end_date+"' "
                                   "AND sc_day_work.create_user='"+str(user_id)+"'")

    return data