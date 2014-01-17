# coding:utf-8
from flask import Module, session, request, render_template, redirect, url_for
from scapp import app

# 信贷工作流程列表
@app.route('/Report/xdgzlclb', methods=['GET'])
def Report_xdgzlclb():
    return render_template("Report/xdgzlclb.html")

