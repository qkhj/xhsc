# coding:utf-8
from flask import Module, session, request, render_template, redirect, url_for, flash
from scapp import app
from scapp import db
from scapp.config import logger
from scapp.models import SC_Loan_Product

# 业务参数配置
@app.route('/System/ywcspz', methods=['GET'])
def System_ywcspz():
    loan_product = SC_Loan_Product.query.all()
    return render_template("System/ywcspz.html",loan_product=loan_product)

# 新增产品
@app.route('/System/new_cp', methods=['GET','POST'])
def new_cp():
    if request.method =='POST':
        try:
            SC_Loan_Product(request.form['product_name'],request.form['max_deadline'],request.form['min_amount'],
                            request.form['max_amount'],request.form['product_describe']).add()
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
    
        return redirect("System/ywcspz")
    else:
        return render_template("System/new_cp.html")

# 修改产品
@app.route('/System/edit_cp/<int:id>', methods=['GET','POST'])
def edit_cp(id):
    if request.method =='POST':
        try:
            loan_product = SC_Loan_Product.query.filter_by(id=id).first()
            loan_product.product_name = request.form['product_name']
            loan_product.max_deadline = request.form['max_deadline']
            loan_product.min_amount = request.form['min_amount']
            loan_product.max_amount = request.form['max_amount']
            loan_product.product_describe = request.form['product_describe']
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
    
        return redirect("System/ywcspz")
    else:
        loan_product = SC_Loan_Product.query.filter_by(id=id).first()
        return render_template("System/edit_cp.html",loan_product=loan_product)