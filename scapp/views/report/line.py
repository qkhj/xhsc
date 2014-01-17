# coding:utf-8
from flask import Module, session, request, render_template, redirect, url_for
from scapp import app

# 折线图
@app.route('/Report/line', methods=['GET'])
def Report_line():
    return render_template("Report/line.html")

