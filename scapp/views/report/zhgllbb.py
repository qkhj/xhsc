# coding:utf-8
from flask import Module, session, request, render_template, redirect, url_for
from scapp import app

# 总行管理类报表
@app.route('/Report/zhgllbb', methods=['GET'])
def Report_zhgllbb():
    return render_template("Report/zhgllbb.html")

