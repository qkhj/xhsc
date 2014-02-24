# coding:utf-8
__author__ = 'johhny'

from scapp import app,db
from flask import request,render_template,flash,redirect,Response
from scapp.config import PER_PAGE,logger
from scapp.models.cust_mgr.sc_day_work import SC_Day_Work
from scapp.models import SC_UserRole
from flask_login import current_user
from sqlalchemy import and_
from scapp.tools.export_excel import export_excel
import datetime,time,xlwt

ezxf=xlwt.easyxf #样式转换

# 客户经理工时新增
@app.route('/Cust_mgr/add', methods=['GET','POST'])
def new_cust_mgr():
    if request.method=='POST':
        try:
            date=datetime.datetime.now()

            work_type=request.form['work_type']
            work_type_detail=request.form['work_type_detail']
            s_beg_date=request.form['beg_date']
            s_beg_time=time.strptime(s_beg_date,'%H:%M')
            beg_date=date.replace(hour=s_beg_time.tm_hour,minute=s_beg_time.tm_min)
            s_end_date=request.form['end_date']
            s_end_time=time.strptime(s_end_date,'%H:%M')
            end_date=date.replace(hour=s_end_time.tm_hour,minute=s_end_time.tm_min)
            time_consume=request.form['time_consume']
            remark=request.form['remark']

            SC_Day_Work(work_type,work_type_detail,beg_date,end_date,time_consume,remark).add()

            # 事务提交
            db.session.commit()
            # 消息闪现
            flash('保存成功','success')
        except:
            # 回滚
            db.session.rollback()
            logger.exception('error')
            # 消息闪现
            flash('保存失败','error')

        return redirect('/Cust_mgr/add')

    elif request.method=='GET':
        return render_template('/Information/gsjl/new_gsjl.html')


# 客户经理工时查询,查询界面
@app.route('/Cust_mgr/search', methods=['GET','POST'])
def show_cust_mgr_search():
    user=db.engine.execute("SELECT * FROM view_get_cus_mgr WHERE role_level>='2'")
    return render_template('/Information/gsjl/gsjl_search.html',user=user)

# 客户经理工时查询,查询结果
@app.route('/Cust_mgr/search_result/<int:page>', methods=['GET','POST'])
def cust_mgr_search_result(page):

    if request.method=='GET':
		user_id=request.args.get('yunying_loan_officer',None)
		s_beg_date=str(request.args.get('beg_date','1999-01-01'))
		s_end_date=str(request.args.get('end_date','2999-01-01'))
		beg_date=datetime.datetime.strptime(s_beg_date,'%Y-%m-%d')
		end_date=datetime.datetime.strptime(s_end_date,'%Y-%m-%d')
		end_date=end_date.replace(hour=23,minute=59,second=59)

		data=query_data(page,beg_date,end_date,user_id,'PAGE')

		return render_template('/Information/gsjl/gsjl.html',data=data,beg_date=beg_date,end_date=end_date,user_id=user_id)
    elif request.method=='POST':
        user_id=request.form['yunying_loan_officer']
        s_beg_date=str(request.form['beg_date'])
        s_end_date=str(request.form['end_date'])
        beg_date=datetime.datetime.strptime(s_beg_date,'%Y-%m-%d %H:%M:%S')
        end_date=datetime.datetime.strptime(s_end_date,'%Y-%m-%d %H:%M:%S')
        end_date=end_date.replace(hour=23,minute=59,second=59)

        data=query_data(page,s_beg_date,s_end_date,user_id)

        exl_hdngs=['日期','姓名','工作类型','工作名称','工作开始时间','工作结束时间','耗时','备注']
        types=     'date   text   text      text      datetime     datetime    text   text'.split()
        exl_hdngs_xf=ezxf('font: bold on;align: wrap on,vert centre,horiz center')
        types_to_xf_map={
            'int':ezxf(num_format_str='#,##0'),
            'date':ezxf(num_format_str='yyyy-mm-dd'),
            'datetime':ezxf(num_format_str='yyyy-mm-dd HH:MM:SS'),
            'ratio':ezxf(num_format_str='#,##0.00%'),
            'text':ezxf(),
            'price':ezxf(num_format_str='￥#,##0.00')
        }

        data_xfs=[types_to_xf_map[t] for t in types]
        date=datetime.datetime.now()
        year=date.year
        month=date.month
        day=date.day
        filename=str(year)+'_'+str(month)+'_'+str(day)+'_'+'客户经理工时统计表'+'.xls'
        exp=export_excel()
        return exp.export_download(filename,'客户经理工时统计表',exl_hdngs,data,exl_hdngs_xf,data_xfs)

def query_data(page,beg_date,end_date,user_id,type='NOPAGE'):
    userrole=SC_UserRole.query.filter_by(user_id=current_user.id).first()
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
                                                   SC_Day_Work.create_user==current_user.id)).paginate(page, per_page = PER_PAGE)
            else:
                data=db.engine.execute("select sc_day_work.create_date,sc_user.real_name as create_user,sc_day_work.work_type,"
                                   "sc_day_work.work_type_detail,sc_day_work.beg_date,sc_day_work.end_date,"
                                   "sc_day_work.time_consume,sc_day_work.remark "
                                   "from sc_day_work "
                                   "inner join sc_user ON sc_day_work.create_user=sc_user.id "
                                   "where sc_day_work.create_date between '"+beg_date+"' AND '"+end_date+"' "
                                   "AND sc_day_work.create_user="+current_user.id+"")
    else:
        if type=='PAGE':
            data=SC_Day_Work.query.filter(and_(SC_Day_Work.create_date.between(beg_date,end_date),
                                          SC_Day_Work.create_user==user_id,SC_Day_Work.create_user==current_user.id)).paginate(page, per_page = PER_PAGE)
        else:
            data=db.engine.execute("select sc_day_work.create_date,sc_user.real_name as create_user,sc_day_work.work_type,"
                                   "sc_day_work.work_type_detail,sc_day_work.beg_date,sc_day_work.end_date,"
                                   "sc_day_work.time_consume,sc_day_work.remark "
                                   "from sc_day_work "
                                   "inner join sc_user ON sc_day_work.create_user=sc_user.id "
                                   "where sc_day_work.create_date between '"+beg_date+"' AND '"+end_date+"' "
                                   "AND sc_day_work.create_user='"+user_id+"' "
                                   "AND sc_day_work.create_user='"+current_user.id+"'")

    return data