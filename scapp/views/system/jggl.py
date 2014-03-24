# coding:utf-8
from scapp import db
from scapp.config import logger
import scapp.helpers as helpers
import datetime

from flask import Module, session, request, render_template, redirect, url_for, flash
from flask.ext.login import current_user

from scapp.models import SC_Org

from scapp import app

# 机构管理
@app.route('/System/jggl', methods=['GET'])
def System_jggl():
    return render_template("System/jggl.html")

# 加载树
@app.route('/System/tree/SC_Org', methods=['GET','POST'])
def init_org_tree():
    # 加载所有
    tree = SC_Org.query.order_by("id").all()
    return helpers.show_result_content(tree) # 返回json
	
# 新增机构
@app.route('/System/new_jggl/<int:pId>', methods=['GET','POST'])
def new_jggl(pId):
    if request.method == 'POST':
        try:
            SC_Org(request.form['name'],request.form['level'],pId).add()

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

        return redirect('System/jggl')
    else:
        return render_template("System/new_jggl.html",pId=pId)

# 编辑机构
@app.route('/System/edit_jggl/<int:id>', methods=['GET','POST'])
def edit_jggl(id):
    if request.method == 'POST':
        try:
            obj = SC_Org.query.filter_by(id=id).first()
            obj.name = request.form['name']
            obj.level = request.form['level']

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

        return redirect('System/jggl')
    else:
        obj = SC_Org.query.filter_by(id=id).first()
        return render_template("System/edit_jggl.html",obj=obj)
            
# 编辑机构
@app.route('/System/delete_jggl/<int:id>', methods=['GET','POST'])
def delete_jggl(id):
    try:
        SC_Org.query.filter_by(id=id).delete()

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

    return redirect('System/jggl')