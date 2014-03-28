# coding:utf-8
__author__ = 'johhny'

from scapp import app,db
from flask import request,render_template,flash,redirect,Response
from scapp.config import PER_PAGE,logger
from scapp.models.cust_mgr.sc_day_work import SC_Day_Work
from scapp.models import SC_UserRole
from flask_login import current_user
from scapp.tools.export_excel import export_excel
import datetime,time,xlwt,re

from scapp.logic.cust_mgr import sc_day_work

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
        return render_template('/Performance/gsjl/new_gsjl.html')


# 客户经理工时查询,查询界面
@app.route('/Cust_mgr/search', methods=['GET','POST'])
def show_cust_mgr_search():
    user=db.engine.execute("SELECT * FROM view_get_cus_mgr WHERE role_level>='2'")
    return render_template('/Performance/gsjl/gsjl_search.html',user=user)

# 客户经理工时查询,查询结果
@app.route('/Cust_mgr/search_result/<int:page>', methods=['GET','POST'])
def cust_mgr_search_result(page):

    if request.method=='GET':
        user_id=request.args.get('yunying_loan_officer',None)
        s_beg_date=str(request.args.get('beg_date','1999-01-01'))
        s_end_date=str(request.args.get('end_date','2999-01-01'))
        r_beg_date = re.search('\d\d\d\d-\d\d-\d\d', s_beg_date).group()
        r_end_date = re.search('\d\d\d\d-\d\d-\d\d', s_end_date).group()
        beg_date=datetime.datetime.strptime(r_beg_date,'%Y-%m-%d')
        end_date=datetime.datetime.strptime(r_end_date,'%Y-%m-%d')
        end_date=end_date.replace(hour=23,minute=59,second=59)

        data=sc_day_work.get_data_by_conditions(page,beg_date,end_date,user_id,current_user.id,'PAGE')


        return render_template('/Performance/gsjl/gsjl.html',data=data,beg_date=beg_date,end_date=end_date,user_id=user_id)
    elif request.method=='POST':
        user_id=request.form['yunying_loan_officer']
        s_beg_date=str(request.form['beg_date'])
        s_end_date=str(request.form['end_date'])
        beg_date=datetime.datetime.strptime(s_beg_date,'%Y-%m-%d %H:%M:%S')
        end_date=datetime.datetime.strptime(s_end_date,'%Y-%m-%d %H:%M:%S')
        end_date=end_date.replace(hour=23,minute=59,second=59)

        data=sc_day_work.get_data_by_conditions(page,s_beg_date,s_end_date,user_id,current_user.id)


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

# 个人薪酬——搜索
@app.route('/Performance/jxxc/grxc_search', methods=['GET'])
def grxc_search():
    return render_template("Performance/jxxc/grxc_search.html")

# 个人薪酬
@app.route('/Performance/jxxc/grxc', methods=['GET'])
def grxc():
    return render_template("Performance/jxxc/grxc.html")

# 薪酬查询——搜索
@app.route('/Performance/jxxc/xccx_search', methods=['GET'])
def xccx_search():
    return render_template("Performance/jxxc/xccx_search.html")

# 薪酬查询
@app.route('/Performance/jxxc/xccx', methods=['GET'])
def xccx():
    return render_template("Performance/jxxc/xccx.html")

# 薪酬详单——搜索
@app.route('/Performance/jxxc/xcxd_search', methods=['GET'])
def xcxd_search():
    return render_template("Performance/jxxc/xcxd_search.html")

# 薪酬详单
@app.route('/Performance/jxxc/xcxd', methods=['GET'])
def xcxd():
    return render_template("Performance/jxxc/xcxd.html")

# 风险保证金——搜索
@app.route('/Performance/jxxc/fxbzj_search', methods=['GET'])
def fxbzj_search():
    return render_template("Performance/jxxc/fxbzj_search.html")

# 风险保证金
@app.route('/Performance/jxxc/fxbzj', methods=['GET'])
def fxbzj():
    return render_template("Performance/jxxc/fxbzj.html")

# 层级查询——搜索
@app.route('/Performance/khjlgl/cjcx_search', methods=['GET'])
def cjcx_search():
    return render_template("Performance/khjlgl/cjcx_search.html")

# 层级查询
@app.route('/Performance/khjlgl/cjcx', methods=['GET'])
def cjcx():
    return render_template("Performance/khjlgl/cjcx.html")

# 晋级审核——搜索
@app.route('/Performance/khjlgl/jjsh_search', methods=['GET'])
def jjsh_search():
    return render_template("Performance/khjlgl/jjsh_search.html")

# 晋级审核列表
@app.route('/Performance/khjlgl/jjshlist', methods=['GET'])
def jjshlist():
    return render_template("Performance/khjlgl/jjshlist.html")

# 晋级审核
@app.route('/Performance/khjlgl/jjsh', methods=['GET'])
def jjsh():
    return render_template("Performance/khjlgl/jjsh.html")

# 层级评估
@app.route('/Performance/khjlgl/cjpg', methods=['GET'])
def cjpg():
    return render_template("Performance/khjlgl/cjpg.html")